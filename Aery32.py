import sublime, sublime_plugin
import os, zipfile, json

class AeryNewProject(sublime_plugin.WindowCommand):
	location = None

	def run(self, *args, **kwargs):
		self.settings = sublime.load_settings('Aery32.sublime-settings')
		self.pm = PrerequisitiesManager()

		try:
			self.pm.install_fetch()
			self.pm.install_sublimeclang()
		except:
			sublime.error_message('ERROR: Could not install prerequisities which are Nettuts+ Fetch and SublimeClang.')
			return False

		initial_location = os.path.expanduser('~')
		if self.window.folders():
			initial_location = self.window.folders()[0]

		# Prompt location where to create a new project
		self.window.show_input_panel(
			"Create new project to: ",
			initial_location,
			self.create,
			None,
			None
		)

	def create(self, location):
		if not os.path.exists(location):
			try:
				os.makedirs(location)
			except:
				sublime.error_message('ERROR: Could not create directory.')
				return False

		self.location = location

		# Download Aery32 framework using Fetch plugin
		self.window.active_view().run_command("fetch_get", {
			"option": "package",
			"url": self.settings.get("download_url"),
			"location": location
		})

		# WORKAROUND, waiting a feature to fetch plug-in
		# https://github.com/weslly/Nettuts-Fetch/issues/12
		sublime.set_timeout(self.configure, 10000)

	def configure(self):
		if not self.location:
			return

		pfile_path = os.path.join(self.location, "Aery32.sublime-project")

		pfile = open(pfile_path, 'r')
		psettings = json.load(pfile)
		pfile.close()

		psettings["settings"].update(SUBLIMECLANG_SETTINGS)

		pfile = open(pfile_path, 'w')
		pfile.write(json.dumps(psettings, sort_keys=False, indent=4))
		pfile.close()

		if self.settings.get("strip", True):
			self.strip()

		# IMPLEMENT! Open Aery32.sublime-project into new Window

		# IMPLEMENT! Open board.cpp and main.cpp files into tabs

	def strip(self):
		""" Cleans the downloaded project from less important files """
		if not self.location:
			return
		for f in [".travis.yml", ".gitignore", "README.md"]:
			os.remove(os.path.join(self.location, f))


class PrerequisitiesManager():
	""" Install fetch and SublimeClang plugins if necessary """
	fetch_path = None
	sublimeclang_path = None

	def __init__(self):
		from os.path import dirname, abspath, join
		self.pwd = dirname(abspath(__file__))
		self.fetch_path = join(sublime.packages_path(), "Nettuts+ Fetch")
		self.sublimeclang_path = join(sublime.packages_path(), "SublimeClang")

	def install_fetch(self):
		if os.path.exists(self.fetch_path):
			return
		f = zipfile.ZipFile(os.path.join(self.pwd, "Nettuts+ Fetch.zip"))
		f.extractall(sublime.packages_path())

	def install_sublimeclang(self):
		if os.path.exists(self.sublimeclang_path):
			return
		f = zipfile.ZipFile(os.path.join(self.pwd, "SublimeClang.zip"))
		f.extractall(sublime.packages_path())

		# IMPLEMENT! Remember to disable SublimeClang plugin by default (from user-settings)


def which(executable):
	""" Mimics Linux / Unix Command: which """
	from os.path import join, isfile
	
	for path in os.environ['PATH'].split(os.pathsep):
		target = join(path, executable)
		if isfile(target) or isfile(target + '.exe'):
			return path
	return None

def dump_cpp_defines(gcc, mpart):
	""" Returns C preprocessor defines as a list """
	cmd = "%s -mpart=%s -dM -E - < %s" % (gcc, mpart, os.devnull)
	return os.popen(cmd).readlines()

def cnv_cpp_define_to_optflag(define):
	""" Returns C preprocessor define converted to GCC option flag """
	import re
	try:
		m = re.search(r"#define (\w+) ([a-zA-Z0-9_() -]+)", define)
		identifier = m.group(1)
		replacement = m.group(2)
		if ' ' in replacement:
			replacement = "\"%s\"" % replacement
	except:
		try:
			m = re.search(r"#define (\w+)", define)
			identifier = m.group(1)
		except:
			return None

	if 'replacement' in locals():
		return "-D%s=%s" % (identifier, replacement)
	else:
		return "-D%s" % identifier

def cnv_cpp_defines_to_optflags(defines):
	for i, define in enumerate(defines):
		input_optflag = cnv_cpp_define_to_optflag(define)
		defines[i] = input_optflag
	return defines

def sublpath(path):
	import string

	if len(path) < 2:
		return
	if path[1] != ":":
		return path
	path = string.replace(path, ':', '')
	path = string.replace(path, '\\', '/')
	return '/%s' % path

AVR_TOOLCHAIN_PATH = os.path.join(which('avr32-g++'), '..')
SUBLIMECLANG_SETTINGS = {
	"sublimeclang_enabled": "true",
	"sublimeclang_options": [
		"-Wall", "-Wno-attributes",
		"-ccc-host-triple", "mips",
		"-I${project_path:aery32}",
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/avr32/include"),
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/lib/gcc/avr32/4.4.3/include"),
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/lib/gcc/avr32/4.4.3/include-fixed"),
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/lib/gcc/avr32/4.4.3/include/c++"),
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/lib/gcc/avr32/4.4.3/include/c++/avr32")
	] + cnv_cpp_defines_to_optflags(dump_cpp_defines('avr32-g++', 'uc3a1128')),
	"sublimeclang_dont_prepend_clang_includes": "true",
	"sublimeclang_show_output_panel": "true",
	"sublimeclang_show_status": "true",
	"sublimeclang_show_visual_error_marks": "true"
}
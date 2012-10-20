import sublime, sublime_plugin
import os, zipfile

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

		# Prompt location where to create a new project
		initial_location = os.path.expanduser('~')
		if self.window.folders():
			initial_location = self.window.folders()[0]

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
				self.location = location
			except:
				sublime.error_message('ERROR: Could not create directory.')
				return False

		# Download Aery32 framework using Fetch plugin
		self.window.active_view().run_command("fetch_get", {
			"option": "package",
			"url": self.settings.get("download_url"),
			"location": location
		})

		# Wait fetch to complete by using timeout function. Or wait callback?
		# https://github.com/weslly/Nettuts-Fetch/issues/12

	def configure(self, location):
		if self.settings.get("strip", True):
			self.strip(location)

		# Set SublimeClang Settings into Aery32.sublime-project

		# Open Aery32.sublime-project into new Window

		# Open board.cpp and main.cpp files into tabs

	def strip(self, location):
		""" Cleans the downloaded project from less important files """

		for f in [".travis.yml", ".gitignore", "README.md"]:
			os.remove(os.path.join(location, f))


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

		# Remember to disable SublimeClang plugin by default (from user-settings) if it wasn't installed


def which(executable):
	""" Mimics Linux / Unix Command: which """
	from os.path import join, isfile
	
	for path in os.environ['PATH'].split(os.pathsep):
		target = join(path, executable)
		if isfile(target) or isfile(target + '.exe'):
			return path
	return None

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

SublimeClangSettings = {
	"sublimeclang_enabled": "true",
	"sublimeclang_options": [
		"-Wall", "-Wno-attributes",
		"-ccc-host-triple", "mips",
		"-I${project_path:aery32}",
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/avr32/include"),
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/lib/gcc/avr32/4.4.3/include"),
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/lib/gcc/avr32/4.4.3/include-fixed"),
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/lib/gcc/avr32/4.4.3/include/c++"),
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/lib/gcc/avr32/4.4.3/include/c++/avr32"),
		"-D__AVR32_UC3A1128__",
		"-D__GNUC__=4",
		"-D__SCHAR_MAX__=127",
		"-D__INT_MAX__=2147483647",
		"-D__SHRT_MAX__=32767",
		"-DF_CPU=66000000UL"
	],
	"sublimeclang_dont_prepend_clang_includes": "true",
	"sublimeclang_show_output_panel": "true",
	"sublimeclang_show_status": "true",
	"sublimeclang_show_visual_error_marks": "true"
}
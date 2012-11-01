import sublime, sublime_plugin
import os, shutil, zipfile, json

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

class AeryNewProject(sublime_plugin.WindowCommand):
	settings = None
	location = None

	def run(self, *args, **kwargs):
		self.settings = sublime.load_settings('Aery32.sublime-settings')
		self.pm = PrerequisitiesManager()

		self.pm.install_fetch()
		self.pm.install_sublimeclang()

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
		try:
			os.makedirs(location)
		except:
			sublime.error_message('ERROR: Directory already exists or cannot be created.')
			return False

		self.location = location

		# Download Aery32 framework using Fetch plugin
		self.window.run_command("fetch_get", {
			"option": "package",
			"url": self.settings.get("download_url"),
			"location": location
		})

		self.configure()

	def configure(self):
		if not self.location:
			return

		pfile_path = os.path.join(self.location, "aery32.sublime-project")

		try:
			pfile = open(pfile_path, 'r')
			psettings = json.load(pfile)
			pfile.close()
		except:
			# WORKAROUND, waiting a feature to fetch plug-in
			# https://github.com/weslly/Nettuts-Fetch/issues/12
			sublime.set_timeout(self.configure, 1000)
			return

		psettings["settings"].update(SUBLIMECLANG_SETTINGS)

		pfile = open(pfile_path, 'w')
		pfile.write(json.dumps(psettings, sort_keys=False, indent=4))
		pfile.close()

		# Strip the project by removing less important files or folders
		for item in self.settings.get("strip", []):
			if os.path.isfile(item):
				os.remove(os.path.join(self.location, item))
			elif os.path.isdir(item):
				shutil.rmtree(os.path.join(self.location, item))

		# WAITING FOR FEATURE! Open aery32.sublime-project into new Window
		# http://sublimetext.userecho.com/topic/133328-/
		#self.window.open_project(pfile_path)


class PrerequisitiesManager():
	""" Install fetch and SublimeClang plugins if necessary """
	fetch_path = None
	sublimeclang_path = None

	def __init__(self):
		self.fetch_path = os.path.join(sublime.packages_path(), "Nettuts+ Fetch")
		self.sublimeclang_path = os.path.join(sublime.packages_path(), "SublimeClang")

	def install_fetch(self):
		if os.path.exists(self.fetch_path):
			return
		zf = zipfile.ZipFile(os.path.join(SCRIPT_PATH, "Nettuts+ Fetch.sublime-package"))
		zf.extractall(self.fetch_path)
		zf.close()

	def install_sublimeclang(self):
		if os.path.exists(self.sublimeclang_path):
			return
		zf = zipfile.ZipFile(os.path.join(SCRIPT_PATH, "SublimeClang.sublime-package"))
		zf.extractall(self.sublimeclang_path)
		zf.close()

		# Disable SublimeClang plugin by default (from user-settings)
		f = open(os.path.join(sublime.packages_path(), "User/SublimeClang.sublime-settings"), 'w')
		f.write(json.dumps({"enabled": False}, indent=4))
		f.close()


def which(executable):
	""" Mimics Linux / Unix Command: which """
	from os.path import join, isfile
	
	for path in os.environ['PATH'].split(os.pathsep):
		target = join(path, executable)
		if isfile(target) or isfile(target + '.exe'):
			return path
	return None

def dump_cdefs(gcc, flags = None):
	""" Returns C preprocessor defines as a list """
	if flags:
		cmd = "%s %s -dM -E - < %s" % (gcc, flags, os.devnull)
	else:
		cmd = "%s -dM -E - < %s" % (gcc, os.devnull)
	return os.popen(cmd).readlines()

def cdef_to_gccflag(define):
	""" Returns C preprocessor define converted to GCC option flag """
	import re
	try:
		m = re.search(r"#define (\w+) (.+)", define)
		identifier = m.group(1)
		replacement = m.group(2)
	except:
		try:
			m = re.search(r"#define (\w+)", define)
			identifier = m.group(1)
		except:
			return None

	if 'replacement' in locals():
		return "-D%s=%s" % (identifier, replacement)

	return "-D%s" % identifier

AVR_TOOLCHAIN_PATH = os.path.join(which('avr32-g++'), '..')

PREPROCESSOR_DEFINES = [cdef_to_gccflag(d) for d in dump_cdefs('avr32-g++', '-mpart=uc3a1128')]

# WORKAROUND! These defines rise a warning. Reported to Atmel.
BAD_PREPROCESSOR_DEFINES = [
	"-D__GNUC_PATCHLEVEL__=3",
	"-D__LDBL_MAX__=1.7976931348623157e+308L",
	"-D__USER_LABEL_PREFIX__",
	"-D__LDBL_MIN__=2.2250738585072014e-308L",
	"-D__REGISTER_PREFIX__",
	"-D__VERSION__=\"4.4.3\"",
	"-D__SIZE_TYPE__=long unsigned int",
	"-D__LDBL_EPSILON__=2.2204460492503131e-16L",
	"-D__CHAR16_TYPE__=short unsigned int",
	"-D__WINT_TYPE__=unsigned int",
	"-D__GNUC_MINOR__=4",
	"-D__LDBL_DENORM_MIN__=4.9406564584124654e-324L",
	"-D__PTRDIFF_TYPE__=long int"
]

SUBLIMECLANG_SETTINGS = {
	"sublimeclang_enabled": True,
	"sublimeclang_dont_prepend_clang_includes": True,
	"sublimeclang_show_output_panel": True,
	"sublimeclang_show_status": True,
	"sublimeclang_show_visual_error_marks": True,
	"sublimeclang_options": [
		"-Wall", "-Wno-attributes",
		"-ccc-host-triple", "mips",
		"-I${project_path:aery32}",
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/avr32/include"),
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/lib/gcc/avr32/4.4.3/include"),
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/lib/gcc/avr32/4.4.3/include-fixed"),
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/lib/gcc/avr32/4.4.3/include/c++"),
		"-I" + os.path.normpath(AVR_TOOLCHAIN_PATH + "/lib/gcc/avr32/4.4.3/include/c++/avr32")
	] + [d for d in PREPROCESSOR_DEFINES if not d in BAD_PREPROCESSOR_DEFINES]
}

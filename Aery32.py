import sublime, sublime_plugin
import os, shutil, zipfile, json

def which(executable):
	""" Mimics Linux / Unix Command: which """
	from os.path import join, isfile

	for path in os.environ['PATH'].split(os.pathsep):
		target = join(path, executable)
		if isfile(target) or isfile(target + '.exe'):
			return path
	return None

def gcc_version(gcc):
	""" Returns GCC version in string """
	version = ""
	try:
		version = os.popen("%s --version" % gcc).readline().split()[-1]
	except:
		pass
	return version

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
PATH_TO_AVR32GPP = which("avr32-g++")
AVR32GPP_VERSION = gcc_version("avr32-g++")

class AeryNewProjectCommand(sublime_plugin.WindowCommand):
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
			dialog = 'Location "%s" already exists. Still want to start Aery32 project there?' % location
			if not sublime.ok_cancel_dialog(dialog):
				return

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

		mpart = self.settings.get("mpart", "uc3a1128")
		strip = self.settings.get("strip", [])
		project = os.path.join(self.location, "aery32.sublime-project")

		try:
			pfile = open(project, 'r')
			pfile.close()
		except:
			# WORKAROUND, waiting a feature to fetch plug-in
			# https://github.com/weslly/Nettuts-Fetch/issues/12
			sublime.set_timeout(self.configure, 1000)
			return

		# Setup SublimeClang project file settings
		self.window.run_command("aery_setup_sublimeclang", {
			"mpart": mpart,
			"project": project
		})

		# Strip the project by removing less important files or folders
		for item in strip:
			if os.path.isfile(item):
				os.remove(os.path.join(self.location, item))
			elif os.path.isdir(item):
				shutil.rmtree(os.path.join(self.location, item))

		# WAITING FOR FEATURE! Open aery32.sublime-project into new Window
		# http://sublimetext.userecho.com/topic/133328-/
		#self.window.open_project(project)


class AerySetupSublimeclangCommand(sublime_plugin.WindowCommand):
	def run(self, *args, **kwargs):
		self.settings = sublime.load_settings('Aery32.sublime-settings')

		if not PATH_TO_AVR32GPP:
			sublime.status_message("Aery32 Warning: AVR32 Toolchain not set in PATH.")
			return None

		# Resolve project file
		if not "project" in kwargs:
			try:
				project = os.path.join(self.window.folders()[0], "aery32.sublime-project")
			except:
				sublime.status_message("Aery32 Error: Project not found.")
				return False
		else:
			project = kwargs["project"]

		# Resolve mpart
		if not "mpart" in kwargs:
			mpart = self.settings.get("mpart", "uc3a1128")
		else:
			mpart = kwargs["mpart"]

		# Start setup process
		try:
			project_file = open(project, 'r+')
		except IOError as e:
			sublime.status_message("Aery32 Error: I/O error({0}): {1}".format(e.errno, e.strerror))
			return False

		path_to_avrtoolchain = os.path.join(PATH_TO_AVR32GPP, '..')
		sublclang_settings = self.sublclang_settings(mpart, path_to_avrtoolchain)

		project_settings = json.load(project_file)
		project_settings["settings"].update(sublclang_settings)

		try:
			project_file.seek(0)
			project_file.write(json.dumps(project_settings, sort_keys=False, indent=4))
		except:
			pass
		project_file.close()

	def sublclang_settings(self, mpart, path_to_avrtoolchain):
		# WORKAROUND! These defines rise a warning. Reported to Atmel.
		bad_cdefs = [
			"-D__GNUC_PATCHLEVEL__=3",
			"-D__GNUC_PATCHLEVEL__=7",
			"-D__LDBL_MAX__=1.7976931348623157e+308L",
			"-D__USER_LABEL_PREFIX__",
			"-D__LDBL_MIN__=2.2250738585072014e-308L",
			"-D__REGISTER_PREFIX__",
			"-D__VERSION__=\"4.4.3\"",
			"-D__VERSION__=\"4.4.7\"",
			"-D__SIZE_TYPE__=long unsigned int",
			"-D__LDBL_EPSILON__=2.2204460492503131e-16L",
			"-D__CHAR16_TYPE__=short unsigned int",
			"-D__WINT_TYPE__=unsigned int",
			"-D__GNUC_MINOR__=4",
			"-D__LDBL_DENORM_MIN__=4.9406564584124654e-324L",
			"-D__PTRDIFF_TYPE__=long int"
		]
		cdefs = self.dump_cdefs("avr32-g++", "-mpart=" + mpart)
		cdefs = [self.cdef_to_gccflag(d) for d in cdefs]

		return {
			"sublimeclang_enabled": True,
			"sublimeclang_dont_prepend_clang_includes": True,
			"sublimeclang_show_output_panel": True,
			"sublimeclang_hide_output_when_empty": True,
			"sublimeclang_show_status": True,
			"sublimeclang_show_visual_error_marks": True,
			"sublimeclang_options": [
				"-Wall", "-Wno-attributes",
				"-ccc-host-triple", "mips",
				"-I${project_path:aery32}",
				"-include", "${project_path:settings.h}",
				"-I" + os.path.normpath(path_to_avrtoolchain + "/avr32/include"),
				"-I" + os.path.normpath(path_to_avrtoolchain + "/lib/gcc/avr32/" + AVR32GPP_VERSION + "/include"),
				"-I" + os.path.normpath(path_to_avrtoolchain + "/lib/gcc/avr32/" + AVR32GPP_VERSION + "/include-fixed"),
				"-I" + os.path.normpath(path_to_avrtoolchain + "/lib/gcc/avr32/" + AVR32GPP_VERSION + "/include/c++"),
				"-I" + os.path.normpath(path_to_avrtoolchain + "/lib/gcc/avr32/" + AVR32GPP_VERSION + "/include/c++/avr32")
			] + [d for d in cdefs if not d in bad_cdefs]
		}

	def dump_cdefs(self, gcc, flags = None):
		""" Returns C preprocessor defines as a list """
		if flags:
			cmd = "%s %s -dM -E - < %s" % (gcc, flags, os.devnull)
		else:
			cmd = "%s -dM -E - < %s" % (gcc, os.devnull)
		return os.popen(cmd).readlines()

	def cdef_to_gccflag(self, define):
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
		else:
			return "-D%s" % identifier


class AeryFixHudsonCommand(sublime_plugin.WindowCommand):
	def run(self, *args, **kwargs):
		import fixhudson
		if not PATH_TO_AVR32GPP:
			sublime.status_message("[WARNING] Aery32: AVR32 " /
				"Toolchain not set in PATH.")
			return False
		fixhudson.strip_avr32libs(os.path.join(PATH_TO_AVR32GPP, '..'))


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
		zf = zipfile.ZipFile(os.path.join(SCRIPT_PATH, "NettutsFetch-2.0.0.sublime-package"))
		zf.extractall(self.fetch_path)
		zf.close()

	def install_sublimeclang(self):
		if os.path.exists(self.sublimeclang_path):
			return
		zf = zipfile.ZipFile(os.path.join(SCRIPT_PATH, "SublimeClang-1.0.41.sublime-package"))
		zf.extractall(self.sublimeclang_path)
		zf.close()

		# Disable SublimeClang plugin by default (from user-settings)
		f = open(os.path.join(sublime.packages_path(), "User/SublimeClang.sublime-settings"), 'w')
		f.write(json.dumps({"enabled": False}, indent=4))
		f.close()

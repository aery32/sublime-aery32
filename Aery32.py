import sublime, sublime_plugin
import os

class AeryNewProject(sublime_plugin.WindowCommand):
	def run(self, *args, **kwargs):
		self.settings = sublime.load_settings('Aery32.sublime-settings')

		# Where to create a new project
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
			except:
				sublime.error_message('ERROR: Could not create directory.')
				return False

		# Download Aery32 framework using Fetch plugin
		self.window.active_view().run_command("fetch_get", {
			"option": "package",
			"url": self.settings.get("download_url"),
			"location": location
		})

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


class AeryInstallPrerequisitiesCommand(sublime_plugin.WindowCommand):
	""" Install fetch and SublimeClang plugins if necessary """
	
	def run(self, *args, **kwargs):
		pass

	def install_fetch(self, callback):
		pass

	def install_sublimeclang(self, callback):
		pass

		try:
			self.window.active_view().run_command("install_package", {
				"name": "SublimeClang"
			})
			self.window.active_view().run_command("enable_package", {
				"name": "SublimeClang"
			})
		except:
			pass

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
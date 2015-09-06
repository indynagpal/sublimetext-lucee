import sublime_plugin
from os.path import dirname, realpath
from .color_scheme_styles import toggle

__all__ = ["LuceeColorSchemeStylesCommand"]
MODULE_PATH = dirname(realpath(__file__)).replace("\\", "/")

class LuceeDefaultColorSchemeStylesCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.window.run_command("open_file", {"file": "${packages}/" + MODULE_PATH.split("/")[-3] + "/src/color_scheme_styles/lucee_color_scheme_styles.sublime-settings"})

class LuceeColorSchemeStylesCommand(sublime_plugin.ApplicationCommand):

	def run(self):
		toggle()
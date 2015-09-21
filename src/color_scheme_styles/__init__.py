import sublime_plugin
from os.path import dirname, realpath
from .color_scheme_styles import toggle

__all__ = ["LuceeColorSchemeStylesCommand"]
MODULE_PATH = dirname(realpath(__file__)).replace("\\", "/")

class LuceeColorSchemeStylesCommand(sublime_plugin.ApplicationCommand):

	def run(self):
		toggle()
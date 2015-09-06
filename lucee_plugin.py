import sublime, sublime_plugin, webbrowser
from os.path import dirname, realpath, splitext
from .lib import bootstrap
from .lib import cfdocs, color_scheme_styles, events, utils
from .lib import completions

LUCEE_PLUGIN_PATH = dirname(realpath(__file__)).replace("\\", "/")

class LuceeEventListener(sublime_plugin.EventListener):
	"""
	Event Listener for Lucee/CFML
	"""
	def on_load_async(self, view):
		events.trigger('on_load_async', view)

	def on_close(self, view):
		events.trigger('on_close', view)

	def on_post_save_async(self, view):
		events.trigger('on_post_save_async', view)

	def on_query_completions(self, view, prefix, locations):
		for dialect in ["lucee","cfml"]:
			if not view.match_selector(locations[0], "embedding." + dialect):
				continue

			prefix_start = locations[0] - len(prefix)
			base_script_scope = "embedding." + dialect + " source." + dialect + ".script"

			# tag completions
			if view.match_selector(prefix_start, "embedding." + dialect + " - source." + dialect + ".script"):
				tag_completions = completions.get_tag_completions(view, prefix, locations[0], dialect)
				return (tag_completions, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

			# dot completions (member and model function completions)
			if view.match_selector(prefix_start - 1, base_script_scope + " keyword.operator.accessor." + dialect):
				completion_list = completions.get_dot_completions(view, prefix, locations[0], dialect)
				return (completion_list, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

			#tag in script attribute completions
			if view.match_selector(prefix_start, base_script_scope + " meta.tag, " + base_script_scope + " meta.class"):
				attribute_completions = completions.get_script_tag_attributes(view, prefix, locations[0], dialect)
				return (attribute_completions, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

			# script completions
			if view.match_selector(prefix_start, "embedding." + dialect + " source." + dialect + ".script"):
				completion_list = completions.get_script_completions(view, prefix, locations[0], dialect)
				return (completion_list, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

		# default
		return None

class LuceeDocsCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		pt = self.view.sel()[0].begin()
		is_function = self.view.match_selector(pt, "support.function.lucee")
		if is_function:
			word = self.view.substr(self.view.word(pt)).lower()
		else:
			word_region = self.view.expand_by_class(pt, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END, "<:/>")
			word = self.view.substr(word_region).lower()
		full_url = "http://docs.lucee.org/reference/" + ("functions" if is_function else "tags") + "/" + word + ".html"
		webbrowser.open_new_tab(full_url)


class CfdocsCommand(sublime_plugin.TextCommand):

	cfdocs.load(LUCEE_PLUGIN_PATH)

	def run(self, edit):
		pt = self.view.sel()[0].begin()
		doc_name = None

		# functions
		if self.view.match_selector(pt, "support.function.cfml"):
			doc_name = self.view.substr(self.view.word(pt)).lower()

		elif self.view.match_selector(pt, "meta.support.function-call.cfml"):
			doc_name, function_name_region, function_args_region = utils.get_function(self.view, pt, "meta.support.function-call")

		# tags
		elif self.view.match_selector(pt, "meta.tag.cfml,meta.tag.script.cfml"):
			doc_name = utils.get_tag_name(self.view, pt)
			if doc_name[:2] != "cf":
				# tag in script
				doc_name = "cf" + doc_name

		# script component, interface, function
		elif self.view.match_selector(pt, "meta.class.cfml"):
			doc_name = "cfcomponent"
		elif self.view.match_selector(pt, "meta.interface.cfml"):
			doc_name = "cfinterface"
		elif self.view.match_selector(pt, "meta.function.cfml"):
			doc_name = "cffunction"

		if doc_name:
			self.view.show_popup(cfdocs.get_cfdoc(doc_name), max_width=640, max_height=320, on_navigate=self.on_navigate)

	def on_navigate(self, href):
		webbrowser.open_new_tab(href)


class CloseLuceeTagCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		pt = self.view.sel()[0].begin()
		last_open_tag = utils.get_last_open_tag(self.view,pt - 1)
		if last_open_tag:
			self.view.insert(edit,pt,"/" + last_open_tag + ">")
		else:
			# if there is no open tag print "/"
			self.view.insert(edit,pt,"/")

class LuceeDefaultColorSchemeStylesCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.window.run_command("open_file", {"file": "${packages}/" + LUCEE_PLUGIN_PATH.split("/").pop() + "/settings/lucee_color_scheme_styles.sublime-settings"})

class LuceeColorSchemeStylesCommand(sublime_plugin.ApplicationCommand):

	def run(self):
		color_scheme_styles.toggle()
import sublime, sublime_plugin, json, webbrowser
from os.path import dirname, realpath, splitext
from .lib import cfdocs, color_scheme_styles, projectcompletions, utils

LUCEE_PLUGIN_PATH = dirname(realpath(__file__)).replace("\\", "/")

def get_project_name(project_file_name):
	project_file = project_file_name.replace("\\","/").split("/").pop()
	project_name, ext = splitext(project_file)
	return project_name

def get_project_list():
	return [(get_project_name(window.project_file_name()), window.project_data()) for window in sublime.windows() if window.project_file_name()]

def plugin_loaded():
	projectcompletions.sync_projects(get_project_list())


class LuceeCompletions(sublime_plugin.EventListener):
	"""
	Provide completions for Lucee/CFML
	"""
	def __init__(self):
		self.completions = utils.load_completions(LUCEE_PLUGIN_PATH)

	def on_load_async(self, view):
		projectcompletions.sync_projects(get_project_list())

	def on_close(self, view):
		projectcompletions.sync_projects(get_project_list())

	def on_post_save_async(self, view):
		if view.window().project_file_name():
			projectcompletions.load_project_file(get_project_name(view.window().project_file_name()), view.window().project_data(), view.file_name())

	def on_query_completions(self, view, prefix, locations):
		for dialect in ["lucee","cfml"]:
			if not view.match_selector(locations[0], "embedding." + dialect):
				continue

			# tag completions
			if view.match_selector(locations[0], "embedding." + dialect + " - source." + dialect + ".script"):
				return self.get_tag_completions(view, prefix, locations, dialect)

			# member and model function completions
			if view.match_selector(locations[0] - 1, "embedding." + dialect + " source." + dialect + ".script meta.property.object." + dialect + ", embedding." + dialect + " source." + dialect + ".script keyword.operator.accessor." + dialect):
				# are we in a project
				project_file_name = view.window().project_file_name()
				if project_file_name:
					# get previous word
					bean_name = view.substr(view.word(locations[0] - len(prefix) - 1))
					if projectcompletions.has_completions(get_project_name(project_file_name), bean_name):
						return (projectcompletions.get_completions(get_project_name(project_file_name), bean_name), sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
				# if no match to a bean name return the member function completions
				return (self.completions[dialect + "_member_functions"], sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

			# tag in script attribute completions
			if view.match_selector(locations[0] - len(prefix) - 1, "embedding." + dialect + " source." + dialect + ".script meta.tag"):
				completion_list = self.get_attribute_completions(utils.get_tag_name(view, locations[0]), True, dialect)
				return (completion_list, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
			# adding component (i.e. cfcomponent) attribute completions separately so I don't have to rescope
			if view.match_selector(locations[0] - len(prefix) - 1, "embedding." + dialect + " source." + dialect + ".script meta.class"):
				completion_list = self.get_attribute_completions("component", True, dialect)
				return (completion_list, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
			# in all script scopes add a check of last word entered, it might be a tag in script but not yet scoped as such
			if view.match_selector(locations[0], "embedding." + dialect + " source." + dialect + ".script"):
				previous_word = utils.get_previous_word(view, locations[0] - len(prefix) - 1)
				completion_list = self.get_attribute_completions(previous_word, True, dialect)
				if len(completion_list) > 0:
					return (completion_list, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

			# function and tag-in-script completions
			if view.match_selector(locations[0], "embedding." + dialect + " source." + dialect + ".script"):
				completion_list = []
				completion_list.extend(self.completions[dialect + "_functions"])
				completion_list.extend(self.completions[dialect + "_tags_in_script"])
				return (completion_list, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

		# default
		return None

	def get_tag_completions(self, view, prefix, locations, dialect):

		pt = locations[0] - len(prefix) - 1
		ch = view.substr(sublime.Region(pt, pt + 1))
		is_inside_tag = view.match_selector(locations[0],"meta.tag - punctuation.definition.tag.begin")

		if is_inside_tag and ch != "<":
			if ch in [" ", "\t", "\n"]:
				# maybe trying to type an attribute
				completion_list = self.get_attribute_completions(utils.get_tag_name(view, locations[0]), False, dialect)
				return (completion_list, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

		if prefix == "":
			# need completion list to match
			return ([], sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

		completion_list = self.completions[dialect + "_tags"]

		# if the opening < is not here insert that
		if ch != "<":
			completion_list = [(pair[0], "<" + pair[1]) for pair in completion_list]

		return (completion_list, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

	def get_attribute_completions(self, tag_name, tag_in_script, dialect):

		# check that this tag looks valid
		if not tag_name:
			return []

		# tags in script don't have "cf" or ":" prefix
		if tag_in_script:
			tag_name = (":" if dialect == "lucee" else "cf") + tag_name

		# got the tag, now find all attributes that match
		attribute_completions = self.completions[dialect + "_tag_attributes"].get(tag_name, [])
		return attribute_completions


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

		elif self.view.match_selector(pt, "meta.support.function-call.arguments.cfml"):
			doc_name = utils.get_support_function_name(self.view, pt)

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
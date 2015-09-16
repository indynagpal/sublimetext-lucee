import sublime, sublime_plugin, webbrowser
from os.path import dirname, realpath
from . import utils
from collections import namedtuple

Documentation = namedtuple('Documentation', 'doc_html_variables on_navigate type')

FILE_PATH = dirname(realpath(__file__)).replace("\\", "/")
DOC_TEMPLATE = ""

documentation_sources = []

def add_documentation_source(callback):
	documentation_sources.append(callback)

def get_inline_documentation(view, position):
	default_doc = None

	for callback in documentation_sources:
		inline_doc = callback(view, position)
		if inline_doc:
			if inline_doc.type == 'default':
				default_doc = inline_doc
			else:
				return build_doc_html(inline_doc.doc_html_variables), inline_doc.on_navigate

	if default_doc:
		return build_doc_html(default_doc.doc_html_variables), default_doc.on_navigate
	return None, None

def plugin_loaded():
	global DOC_TEMPLATE
	template_path = "/".join(FILE_PATH.split('/')[:-1]) + "/templates/"
	DOC_TEMPLATE = load_template(template_path, "inline_documentation")

def load_template(template_path, filename):
	with open(template_path + filename + ".html", "r") as f:
		html_string = f.read()
	return html_string

def build_links(links):
	html_links = ['<a href="' + link["href"] + '">' + link["text"] + '</a>' for link in links]
	return "<br>".join(html_links)

def build_doc_html(inline_doc):
	inline_doc["links"] = build_links(inline_doc["links"])
	return sublime.expand_variables(DOC_TEMPLATE, inline_doc)

class LuceeInlineDocumentationCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		position = self.view.sel()[0].begin()

		doc_html, on_navigate = get_inline_documentation(self.view, position)

		if doc_html:
			self.view.show_popup(doc_html, max_width=640, max_height=320, on_navigate=on_navigate)

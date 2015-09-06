from . import utils
from collections import namedtuple

CompletionList = namedtuple('CompletionList', 'completions type')
completion_sources = {"tag": [], "tag_attributes": [], "script": [], "dot": []}

def add_completion_source(source_type, callback):
	completion_sources[source_type].append(callback)

def get_completions(source_type, *args):
	full_list = []
	default_list = None

	for callback in completion_sources[source_type]:
		completionlist = callback(*args)
		if completionlist:
			if completionlist.type == 'exclusive':
				return completionlist.completions
			elif completionlist.type == 'default':
				default_list = completionlist.completions
			else:
				full_list.extend(completionlist.completions)

	return full_list if len(full_list) else default_list

def get_tag_completions(view, prefix, position, dialect):
	prefix_start = position - len(prefix)
	ch = view.substr(prefix_start - 1)
	is_inside_tag = view.match_selector(prefix_start, "meta.tag - punctuation.definition.tag.begin")

	if is_inside_tag and ch in [" ", "\t", "\n"]:
		info = {"dialect": dialect, "tag_in_script": False, "tag_name": utils.get_tag_name(view, prefix_start)}
		return get_completions('tag_attributes', view, prefix, position, info)

	info = {"dialect": dialect}
	completions = get_completions('tag', view, prefix, position, info)

	# if the opening < is not here insert that
	if ch != "<":
		completions = [(pair[0], "<" + pair[1]) for pair in completions]

	return completions

def get_script_completions(view, prefix, position, dialect):
	info = {"dialect": dialect}
	return get_completions('script', view, prefix, position, info)

def get_script_tag_attributes(view, prefix, position, dialect):
	prefix_start = position - len(prefix)
	info = {"dialect": dialect, "tag_in_script": True}
	info["tag_name"] = "component" if view.match_selector(prefix_start, "meta.class") else utils.get_tag_name(view, prefix_start)
	return get_completions('tag_attributes', view, prefix, position, info)

def get_dot_completions(view, prefix, position, dialect):
	prefix_start = position - len(prefix)
	info = {"dialect": dialect, "dot_context": utils.get_dot_context(view, prefix_start - 1)}
	return get_completions('dot', view, prefix, position, info)

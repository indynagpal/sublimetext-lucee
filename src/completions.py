from . import utils
from collections import namedtuple

CompletionList = namedtuple("CompletionList", "completions priority exclude_lower_priority")
completion_sources = {"tag": [], "tag_attributes": [], "script": [], "dot": []}

def add_completion_source(source_type, callback):
	completion_sources[source_type].append(callback)

def get_completions(source_type, *args):
	completion_lists = []
	minimum_priority = 0

	for callback in completion_sources[source_type]:
		completionlist = callback(*args)
		if completionlist:
			completion_lists.append(completionlist)
			if completionlist.exclude_lower_priority:
				minimum_priority = completionlist.priority

	full_completion_list = []
	for completionlist in sorted(completion_lists, key=lambda comp_list: comp_list.priority, reverse=True):
		if completionlist.priority >= minimum_priority:
			full_completion_list.extend(completionlist.completions)

	return full_completion_list

def get_base_info(view, dialect):
	file_name = view.file_name().replace("\\", "/").split("/").pop().lower()
	return {"dialect": dialect, "file_name": file_name}

def get_tag_completions(view, prefix, position, dialect):
	info = get_base_info(view, dialect)
	prefix_start = position - len(prefix)
	is_inside_tag = view.match_selector(prefix_start, "meta.tag - punctuation.definition.tag.begin")
	is_tag_name = view.match_selector(prefix_start - 1, "punctuation.definition.tag.begin, entity.name.tag")

	if is_inside_tag and not is_tag_name:
		info.update({"tag_in_script": False, "tag_name": utils.get_tag_name(view, prefix_start), "tag_attribute_name": utils.get_tag_attribute_name(view, prefix_start) })
		return get_completions('tag_attributes', view, prefix, position, info)

	completions = get_completions('tag', view, prefix, position, info)

	# if the opening < is not here insert that
	if view.substr(prefix_start - 1) != "<":
		completions = [(pair[0], "<" + pair[1]) for pair in completions]

	return completions

def get_script_completions(view, prefix, position, dialect):
	info = get_base_info(view, dialect)
	return get_completions('script', view, prefix, position, info)

def get_script_tag_attributes(view, prefix, position, dialect):
	prefix_start = position - len(prefix)
	info = get_base_info(view, dialect)
	info["tag_in_script"] = True
	info["tag_name"] = "component" if view.match_selector(prefix_start, "meta.class") else utils.get_tag_name(view, prefix_start)
	return get_completions('tag_attributes', view, prefix, position, info)

def get_dot_completions(view, prefix, position, dialect):
	prefix_start = position - len(prefix)
	info = get_base_info(view, dialect)
	info["dot_context"] = utils.get_dot_context(view, prefix_start - 1)
	return get_completions('dot', view, prefix, position, info)

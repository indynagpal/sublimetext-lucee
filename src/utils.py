import sublime
from collections import deque, namedtuple
from os.path import dirname, realpath

path_parts = dirname(realpath(__file__)).replace("\\", "/").split("/")
LUCEE_PLUGIN_NAME = path_parts[-1].split(".")[0] if "Installed Packages" in path_parts else path_parts[-2]

Symbol = namedtuple('Symbol', 'name is_function function_region args_region')

def get_plugin_name():
	return LUCEE_PLUGIN_NAME

def get_dialect(view, position):
	return "cfml" if view.match_selector(position, "embedding.cfml") else "lucee"

def get_previous_character(view, position):
	if view.substr(position - 1) in [" ", "\t", "\n"]:
		position = view.find_by_class(position, False, sublime.CLASS_WORD_END | sublime.CLASS_PUNCTUATION_END)
	return position - 1

def get_previous_word(view, position):
	previous_character = get_previous_character(view, position)
	return view.substr(view.word(previous_character)).lower()

def get_scope_region_containing_point(view, pt, scope):
	scope_count = view.scope_name(pt).count(scope)
	if scope_count == 0:
		return None
	scope_to_find = " ".join([scope] * scope_count)
	for r in view.find_by_selector(scope_to_find):
		if r.contains(pt):
			return r
	return None

def get_char_point_before_scope(view, pt, scope):
	scope_region = get_scope_region_containing_point(view, pt, scope)
	if scope_region:
		scope_start = scope_region.begin()
		return get_previous_character(view, scope_start)
	return None

def get_dot_context(view, dot_position):
	context = []

	if view.substr(dot_position) != ".":
		return context

	if view.substr(dot_position - 1) in [" ", "\t", "\n"]:
		dot_position = view.find_by_class(dot_position, False, sublime.CLASS_WORD_END | sublime.CLASS_PUNCTUATION_END)

	for scope_name in ["meta.support.function-call", "meta.function-call"]:
		base_scope_count = view.scope_name(dot_position).count(scope_name)
		scope_to_find = " ".join([scope_name] * (base_scope_count + 1))
		if view.match_selector(dot_position - 1, scope_to_find):
			function_name, name_region, function_args_region = get_function_call(view, dot_position - 1, scope_name == "meta.support.function-call")
			context.append(Symbol(function_name, True, name_region, function_args_region))
			break
	else:
		if view.match_selector(dot_position - 1, "variable, meta.property.object"):
			name_region = view.word(dot_position)
			context.append(Symbol(view.substr(name_region).lower(), False, None, None))

	if len(context) > 0:
		context.extend(get_dot_context(view, name_region.begin() - 1))

	return context

def get_struct_context(view, position):
	context = []

	if not view.match_selector(position, "meta.group.braces.curly"):
		return context

	previous_char_point = get_char_point_before_scope(view, position, "meta.group.braces.curly")
	if not view.match_selector(previous_char_point, "keyword.operator.assignment.cfml,punctuation.separator.key-value.cfml"):
		return context

	previous_char_point = get_previous_character(view, previous_char_point)

	if not view.match_selector(previous_char_point, "meta.property.object.cfml,variable,string.unquoted.label.cfml"):
		return context

	name_region = view.word(previous_char_point)
	context.append(Symbol(view.substr(name_region).lower(), False, None, None))

	if view.match_selector(previous_char_point, "meta.property.object.cfml"):
		context.extend(get_dot_context(view, name_region.begin() - 1))
	else:
		context.extend(get_struct_context(view, name_region.begin()))

	return context

def get_tag_end(view, pos, is_lucee):
	tag_end = view.find("/?>", pos)
	if tag_end:
		if view.match_selector(tag_end.begin(), "punctuation.definition.tag"):
			tag_end_is_lucee = view.match_selector(tag_end.begin(), "punctuation.definition.tag.end.lucee, punctuation.definition.tag.end.cfml")
			if is_lucee == tag_end_is_lucee:
				return tag_end
		return get_tag_end(view, tag_end.end(), is_lucee)
	return None


def get_last_open_tag(view, pos, lucee_only):
	tag_selector = "entity.name.tag.lucee, entity.name.tag.cfml" if lucee_only else "entity.name.tag"
	closed_tags = []
	tag_name_regions = reversed([r for r in view.find_by_selector(tag_selector) if r.end() <= pos])

	for tag_name_region in tag_name_regions:
		# check for closing tag
		if view.substr(tag_name_region.begin() - 1) == "/":
			closed_tags.append(view.substr(tag_name_region))
			continue

		# this is an opening tag
		is_lucee = view.match_selector(tag_name_region.begin(), "entity.name.tag.lucee, entity.name.tag.cfml")
		tag_end = get_tag_end(view, tag_name_region.end(), is_lucee)

		# if no tag end then give up
		if not tag_end:
			return None

		# if tag_end is after cursor position, then ignore it
		if tag_end.begin() > pos:
			continue

		# if tag_end length is 2 then this is a self closing tag so ignore it
		if tag_end.size() == 2:
			continue

		tag_name = view.substr(tag_name_region)

		if tag_name in closed_tags:
			closed_tags.remove(tag_name)
			continue

		# check to exclude cfml tags that should not have a closing tag
		if tag_name in ["cfset","cfelse","cfelseif","cfcontinue","cfbreak","cfthrow","cfrethrow"]:
			continue
		# check to exclude lucee tags that should not have a closing tag
		if tag_name in [":set",":else",":elseif",":continue",":break",":throw",":rethrow"]:
			continue
		# check to exclude html tags that should not have a closing tag
		if tag_name in ["area","base","br","col","command","embed","hr","img","input","link","meta","param","source"]:
			continue

		return tag_name

	return None

def get_tag_name(view, pos):
	dialect = get_dialect(view, pos)
	tag_scope = "meta.tag." + dialect + " - punctuation.definition.tag.begin,meta.tag.script." + dialect + " - punctuation.definition.tag.begin"
	tag_name_scope = "entity.name.tag." + dialect + ",entity.name.tag.script." + dialect
	tag_regions = view.find_by_selector(tag_scope)
	tag_name_regions = view.find_by_selector(tag_name_scope)

	for tag_region, tag_name_region in zip(tag_regions, tag_name_regions):
		if tag_region.contains(pos):
			return view.substr(tag_name_region).lower()
	return None

def get_tag_attribute_name(view, pos):
	dialect = get_dialect(view, pos)
	for scope in ["string.quoted","string.unquoted"]:
		full_scope = "meta.tag." + dialect + " " + scope + ", meta.tag.script." + dialect + " " + scope
		if view.match_selector(pos, full_scope):
			previous_char = get_char_point_before_scope(view, pos, scope)
			break
	else:
		previous_char = get_previous_character(view, pos)

	full_scope = "meta.tag." + dialect + " punctuation.separator.key-value, meta.tag.script." + dialect + " punctuation.separator.key-value"
	if view.match_selector(previous_char, full_scope):
		return get_previous_word(view, previous_char)
	return None

def get_function(view, pt):
	dialect = get_dialect(view, pt)
	function_scope = "meta.function." + dialect
	function_name_scope = "entity.name.function." + dialect + ",entity.name.function.constructor." + dialect
	function_region = get_scope_region_containing_point(view, pt, function_scope)
	if function_region:
		function_name_regions = view.find_by_selector(function_name_scope)
		for function_name_region in function_name_regions:
			if function_region.contains(function_name_region):
				return view.substr(function_name_region).lower(), function_name_region, function_region
	return None

def get_function_call(view, pt, support_function = False):
	function_call_scope = "meta.support.function-call" if support_function else "meta.function-call"
	function_region = get_scope_region_containing_point(view, pt, function_call_scope)
	if function_region:
		function_name_region = view.word(function_region.begin())
		function_args_region = sublime.Region(function_name_region.end(), function_region.end())
		return view.substr(function_name_region).lower(), function_name_region, function_args_region
	return None

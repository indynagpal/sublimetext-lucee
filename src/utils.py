import sublime
from collections import deque, namedtuple
Symbol = namedtuple('Symbol', 'name is_function function_region args_region')

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
			function_name, name_region, function_args_region = get_function(view, dot_position - 1, scope_name)
			context.append(Symbol(function_name, True, name_region, function_args_region))
			break
	else:
		if view.match_selector(dot_position - 1, "variable, meta.property.object"):
			name_region = view.word(dot_position)
			context.append(Symbol(view.substr(name_region).lower(), False, None, None))

	if len(context) > 0:
		context.extend(get_dot_context(view, name_region.begin() - 1))

	return context

def get_last_open_tag(view, pos):
	open_tags = deque()
	tag_starts = [r for r in view.find_by_selector("punctuation.definition.tag.begin") if r.end() <= pos]
	tag_ends = [r for r in view.find_by_selector("punctuation.definition.tag.end") if r.end() <= pos]

	# if lengths don't match don't bother trying to find last open tag
	if len(tag_starts) != len(tag_ends):
		return None

	for tag_start, tag_end in zip(tag_starts, tag_ends):
		tag_name_region = sublime.Region(tag_start.end(), view.find_by_class(tag_start.end(), True, sublime.CLASS_WORD_END, "/>"))
		tag_name = view.substr(tag_name_region)

		# if length is 1 then this is a tag opening punctuation
		if tag_start.size() == 1:

			if tag_end.size() > 1:
				# self closing tag has tag end of size 2 "/>" - skip these
				continue

			# check to exclude cfml tags that should not have a closing tag
			if tag_name in ["cfset","cfelse","cfelseif",":set",":else",":elseif"]:
				continue
			# check to exclude html tags that should not have a closing tag
			if tag_name in ["area","base","br","col","command","embed","hr","img","input","link","meta","param","source"]:
				continue

			open_tags.appendleft(tag_name)

		# if length is 2 then this is a tag closing punctuation
		if tag_start.size() == 2 and tag_name in open_tags:
			open_tags.remove(tag_name)

	return open_tags.popleft() if len(open_tags) > 0 else None

def get_tag_name(view, pos):
	dialect = "cfml" if view.match_selector(pos, "embedding.cfml") else "lucee"
	tag_scope = "meta.tag." + dialect + " - punctuation.definition.tag.begin,meta.tag.script." + dialect + " - punctuation.definition.tag.begin"
	tag_name_scope = "entity.name.tag." + dialect + ",entity.name.tag.script." + dialect
	tag_regions = view.find_by_selector(tag_scope)
	tag_name_regions = view.find_by_selector(tag_name_scope)

	for tag_region, tag_name_region in zip(tag_regions, tag_name_regions):
		if tag_region.contains(pos):
			return view.substr(tag_name_region).lower()
	return None

def get_previous_word(view, pos):
	previous_character = view.substr(pos - 1)
	if previous_character in [" ", "\t", "\n"]:
		pos = view.find_by_class(pos, False, sublime.CLASS_WORD_END | sublime.CLASS_PUNCTUATION_END)
	return (view.substr(view.word(pos)).lower(), False)

def get_function(view, pt, function_call_scope):
	function_region = None
	scope_count = view.scope_name(pt).count(function_call_scope)
	if scope_count == 0:
		return None
	scope_to_find = " ".join([function_call_scope] * scope_count)
	for r in view.find_by_selector(scope_to_find):
		if r.contains(pt):
			function_region = r
			break
	if function_region:
		function_name_region = view.word(function_region.begin())
		function_args_region = sublime.Region(function_name_region.end(), function_region.end())
		return view.substr(function_name_region).lower(), function_name_region, function_args_region
	return None
import sublime, json
from urllib.request import urlopen

def load_completions(plugin_path):
	completions_data = {}
	for filename in ["lucee_tags","lucee_functions","lucee_member_functions","cfml_tags","cfml_functions","cfml_member_functions"]:
		completions_data[filename] = load_json_data(plugin_path, filename)

	# setup completion lists
	completions = {}
	for dialect in ["lucee","cfml"]:
		# tags
		completions[dialect + "_tags"] = []
		completions[dialect + "_tags_in_script"] = []
		completions[dialect + "_tag_attributes"] = {}
		for tag_name in sorted(completions_data[dialect + "_tags"].keys()):
			tag_attributes = completions_data[dialect + "_tags"][tag_name]
			completions[dialect + "_tags"].append(make_tag_completion(tag_name, dialect, tag_attributes[0]))
			completions[dialect + "_tags_in_script"].append(make_tag_completion(tag_name[(1 if dialect == "lucee" else 2):], dialect, tag_attributes[0]))
			completions[dialect + "_tag_attributes"][tag_name] = [(a + '\trequired', a + '="$1"') for a in tag_attributes[0]]
			completions[dialect + "_tag_attributes"][tag_name].extend([(a + '\toptional', a + '="$1"') for a in tag_attributes[1]])

		# functions
		completions[dialect + "_functions"] = [(funct + '\tfn (' + dialect + ')', funct + completions_data[dialect + "_functions"][funct]) for funct in sorted(completions_data[dialect + "_functions"].keys())]

		# member functions
		mem_func_comp = []
		for member_function_type in sorted(completions_data[dialect + "_member_functions"].keys()):
			for funct in sorted(completions_data[dialect + "_member_functions"][member_function_type].keys()):
				mem_func_comp.append( (funct + '\t' + member_function_type + '.fn (' + dialect + ')', funct + completions_data[dialect + "_member_functions"][member_function_type][funct]))
		completions[dialect + "_member_functions"] = mem_func_comp

	return completions

def load_json_data(plugin_path, filename):
	with open(plugin_path + '/json/' + filename + '.json', 'r') as f:
		json_data = f.read()
	return json.loads(json_data)

def make_tag_completion(tag, type, required_attrs):
	attrs = ''
	for index, attr in enumerate(required_attrs, 1):
		attrs += ' ' + attr + '="$' + str(index) + '"'
	return (tag + '\ttag (' + type + ')', tag + attrs)

def get_previous_word(view, pos):
	previous_word_start = view.find_by_class(pos, False, sublime.CLASS_WORD_START)
	previous_word = view.substr(sublime.Region(previous_word_start, pos)).strip().lower()
	return previous_word

def get_tag_name(view, pos):
	# walk backwards from cursor, looking for tag name scope
	for index in range(500):
		if view.match_selector(pos - index,"entity.name.tag"):
			tag_name_region = view.expand_by_class(pos - index, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END, "</>;{}()")
			tag_name = view.substr(tag_name_region).lower()
			return tag_name
		if view.match_selector(pos - index,"punctuation.definition.tag.begin"):
			return None

def get_last_open_tag(view,pos):
	open_tags = []
	tag_starts = view.find_by_selector("punctuation.definition.tag.begin")
	tag_ends = view.find_by_selector("punctuation.definition.tag.end")
	tag_ends_index = 0

	for tag_start in tag_starts:

		# don't need to consider tags after the cursor position
		if tag_start.begin() > pos:
			break

		tag_name_region = sublime.Region(tag_start.end(), view.find_by_class(tag_start.end(), True, sublime.CLASS_WORD_END, "/>"))
		tag_name = view.substr(tag_name_region)

		# if length is 1 then this is a tag opening punctuation
		if tag_start.size() == 1:
			# check tag_ends for end of this tag - assumption is it is the first tag_end after current tag_start
			while tag_ends_index < len(tag_ends) and tag_ends[tag_ends_index].begin() < tag_start.end():
				tag_ends_index += 1

			if tag_ends[tag_ends_index].size() > 1:
				# self closing tag has tag end of size 2 "/>" - skip these
				continue

			# check to exclude cfml tags that should not have a closing tag
			if tag_name in ["cfset","cfelse","cfelseif",":set",":else",":elseif"]:
				continue
			# check to exclude html tags that should not have a closing tag
			if tag_name in ["area","base","br","col","command","embed","hr","img","input","link","meta","param","source"]:
				continue
			open_tags.append(tag_name)

		# if length is 2 then this is a tag closing punctuation
		if tag_start.size() == 2 and tag_name in open_tags:
			open_tags.remove(tag_name)

	return open_tags.pop() if len(open_tags) > 0 else None

def get_support_function_name(view, pt):
	args_region = None
	function_call_arguments_scope = "meta.support.function-call.arguments.cfml"
	scope_count = view.scope_name(pt).count(function_call_arguments_scope)
	scope_to_find = " ".join([function_call_arguments_scope] * scope_count)
	for r in view.find_by_selector(scope_to_find):
		if r.contains(pt):
			args_region = r
			break
	if args_region:
		return view.substr(view.word(args_region.begin()-1)).lower()
	return None
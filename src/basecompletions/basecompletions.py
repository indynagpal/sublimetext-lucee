import json
from os.path import dirname, realpath
from ..completions import CompletionList
from ..inline_documentation import Documentation
from .. import utils

FULL_PATH = dirname(realpath(__file__)).replace("\\", "/")
COMPLETION_FILES = ["lucee_tags","lucee_functions","lucee_member_functions","cfml_tags","cfml_functions","cfml_member_functions"]
DOC_STYLES = {
	"side_color": "#4C9BB0",
	"header_color": "#306B7B",
	"header_bg_color": "#E4EEF1",
	"text_color": "#272B33"
}

completions = {}
cgi = {}

def get_tags(view, prefix, position, info):
	completion_list = completions[info["dialect"] + "_tags"]
	return CompletionList(completion_list, 0, False)

def get_tag_attributes(view, prefix, position, info):
	if not info["tag_name"]:
		return None

	if info["tag_in_script"]:
		 info["tag_name"] = (":" if info["dialect"] == "lucee" else "cf") +  info["tag_name"]

	completion_list = completions[info["dialect"] + "_tag_attributes"].get(info["tag_name"], None)
	return CompletionList(completion_list, 0, False)

def get_script_completions(view, prefix, position, info):
	completion_list = []
	completion_list.extend(completions[info["dialect"] + "_functions"])
	completion_list.extend(completions[info["dialect"] + "_tags_in_script"])
	return CompletionList(completion_list, 0, False)

def get_dot_completions(view, prefix, position, info):

	if len(info["dot_context"]) == 1 and info["dot_context"][0].name == "cgi":
		return CompletionList(completions["cgi"], 1, True)

	completion_list = completions[info["dialect"] + "_member_functions"]
	return CompletionList(completion_list, 0, False)

def get_inline_documentation(view, position):

	if view.match_selector(position, "variable.other.constant"):
		word = view.word(position)
		dot_context = utils.get_dot_context(view, word.begin() - 1)
		if len(dot_context) == 1 and dot_context[0].name == "cgi":
			key = "cgi." + view.substr(word).lower()
			if key in cgi:
				doc = dict(DOC_STYLES)
				doc.update(cgi[key])
				return Documentation(doc, None, 1)

	return None

def load_completions():
	global completions, cgi
	completions_data = {filename: load_json_data(filename) for filename in COMPLETION_FILES}

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
		
		# CGI scope
		cgi = load_json_data("cgi")
		completions["cgi"] = [(scope_variable.split(".").pop().upper() + "\tCGI", scope_variable.split(".").pop().upper()) for scope_variable in sorted(cgi.keys())]

def load_json_data(filename):
	with open(FULL_PATH + '/json/' + filename + '.json', 'r') as f:
		json_data = f.read()
	return json.loads(json_data)

def make_tag_completion(tag, type, required_attrs):
	attrs = ''
	for index, attr in enumerate(required_attrs, 1):
		attrs += ' ' + attr + '="$' + str(index) + '"'
	return (tag + '\ttag (' + type + ')', tag + attrs)
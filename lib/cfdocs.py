import sublime, json, urllib

CFDOCS_TEMPLATE = ""
CFDOCS_PARAM_TEMPLATE = ""
CFDOCS_ERROR_TEMPLATE = ""
CFDOCS_BASE_URL = "https://raw.githubusercontent.com/foundeo/cfdocs/master/data/en/"

def load(plugin_path):
	global CFDOCS_TEMPLATE, CFDOCS_PARAM_TEMPLATE, CFDOCS_ERROR_TEMPLATE
	CFDOCS_TEMPLATE = load_template(plugin_path, "cfdocs")
	CFDOCS_PARAM_TEMPLATE = load_template(plugin_path, "cfdocs_param")
	CFDOCS_ERROR_TEMPLATE = load_template(plugin_path, "cfdocs_error")

def load_template(plugin_path, filename):
	with open(plugin_path + "/templates/" + filename + ".html", "r") as f:
		html_string = f.read()
	return html_string

def get_cfdoc(function_or_tag):
	data, success = fetch_cfdoc(function_or_tag)
	if success:
		return build_cfdoc_html(function_or_tag, data)
	return build_cfdoc_error(function_or_tag, data)

def fetch_cfdoc(function_or_tag):
	full_url = CFDOCS_BASE_URL + function_or_tag  + ".json"

	try:
		json_string = urllib.request.urlopen(full_url).read().decode("utf-8")
	except urllib.error.HTTPError as e:
		data = {"error_message": "Unable to fetch " + function_or_tag + ".json<br>" + str(e)}
		return data, False

	try:
		data = json.loads(json_string)
	except ValueError as e:
		data = {"error_message": "Unable to decode " + function_or_tag + ".json<br>ValueError: " + str(e)}
		return data, False

	return data, True

def build_cfdoc_html(function_or_tag, data):
	variables = { "function_or_tag": function_or_tag, "href": "http://cfdocs.org/" + function_or_tag, "params": "" }
	variables["syntax"] = data["syntax"].replace("<","&lt;").replace(">","&gt;")
	variables["description"] = data["description"].replace("<","&lt;").replace(">","&gt;").replace("\n","<br>")

	if len(data["returns"]) > 0:
		variables["syntax"] += ":" + data["returns"]

	if len(data["params"]) > 0:
		variables["params"] = "<ul>"
		for param in data["params"]:
			param_variables = {"name": param["name"], "description": param["description"].replace("\n","<br>"), "values": ""}
			if len(param["values"]):
				param_variables["values"] = "<em>values:</em> " + ", ".join([str(value) for value in param["values"]])
			variables["params"] += "<li>" + sublime.expand_variables(CFDOCS_PARAM_TEMPLATE, param_variables) + "</li>"
		variables["params"] += "</ul>"

	return sublime.expand_variables(CFDOCS_TEMPLATE, variables)

def build_cfdoc_error(function_or_tag, data):
	return sublime.expand_variables(CFDOCS_ERROR_TEMPLATE, data)
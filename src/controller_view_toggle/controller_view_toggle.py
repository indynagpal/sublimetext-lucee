import json, os, sublime
from .. import utils


def toggle_controller_view(view, position):
	file_info = get_file_info(view.file_name())

	if not file_info:
		return
		
	dialect = utils.get_dialect(view, position)		
	file_type, root_path, containing_folder, relative_path = file_info
	
	if file_type == "controller":
		function_name = get_controller_function(view, position)
		if function_name:
			view_path, view_exists = get_verified_path(root_path + "/" + containing_folder, relative_path + "/" + function_name + get_file_extension("view", dialect))
			if not view_exists:
				view_exists = sublime.ok_cancel_dialog(containing_folder + "/" + view_path + " does not exist, do you want to create it?", "Create")
			if view_exists:
				view.window().open_file(root_path + "/" + containing_folder + "/" + view_path, sublime.FORCE_GROUP)
				
	if file_type == "view":
		controller_path, controller_exists = get_verified_path(root_path + "/" + containing_folder, relative_path + get_file_extension("controller", dialect))
		if controller_exists:
			file_path = root_path + "/" + containing_folder + "/" + controller_path
			if file_path[1] == ":":
				file_path = "/" + file_path[0] + file_path[2:]
			symbol = view.file_name().replace("\\","/").split("/")[-1].split(".")[0]
			row, col = 1, 1
			index_locations = view.window().lookup_symbol_in_index(symbol)

			for full_path, project_path, rowcol in index_locations:
				if full_path == file_path:
					row, col = rowcol
					break

			view.window().open_file(file_path + ":" + str(row) + ":" + str(col), sublime.ENCODED_POSITION | sublime.FORCE_GROUP)

def get_folder_settings(type):
	folder_settings = sublime.load_settings("lucee_package.sublime-settings")
	return folder_settings.get(type)

def get_file_info(filename):
	if not filename:
		return None
		
	filename_parts = filename.replace("\\","/").split("/")

	if len(filename_parts) > 1 and filename_parts[-2].lower() in get_folder_settings("controller_folders"):
		root_path = "/".join(filename_parts[:-2])
		containing_folder = get_folder_name(root_path, get_folder_settings("view_folders"))
		relative_path = filename_parts[-1].split(".")[0].lower()
		return "controller", root_path, containing_folder, relative_path
		
	if len(filename_parts) > 2 and filename_parts[-3].lower() in get_folder_settings("view_folders"):
		root_path = "/".join(filename_parts[:-3])
		containing_folder = get_folder_name(root_path, get_folder_settings("controller_folders"))
		relative_path = filename_parts[-2].lower()
		return "view", root_path, containing_folder, relative_path

	return None
	
def get_folder_name(root_path, folders):
	for folder_name in folders:
		verified_path, path_exists = get_verified_path(root_path, folder_name)
		if path_exists:
			return verified_path
	return ""
	
def get_file_extension(type, dialect):
	if dialect == "lucee":
		return ".lucee"
	if type == "view":
		return ".cfm"
	if type == "controller":
		return ".cfc"
	return None

def get_controller_function(view, position):
	funct_body_scope = "meta.group.braces.curly meta.group.braces.curly"
	funct_declaration_scope = "meta.function"
	function_body_region = utils.get_scope_region_containing_point(view, position, funct_body_scope)
	function_position = None

	if function_body_region:
		funct_regions = view.find_by_selector(funct_declaration_scope)
		for funct_region in reversed(funct_regions):
			if funct_region.end() <= function_body_region.begin():
				function_position = funct_region.begin()
				break
	elif view.match_selector(position, "meta.group.braces.curly meta.function"):
		if view.scope_name(position).count("meta.group.braces.curly") == 1:
			function_position = position

	if function_position:
		return view.substr(utils.get_function(view, function_position)[1])

	return None

def get_verified_path(root_path, rel_path):
	normalized_root_path = root_path.replace("\\","/")
	rel_path_elements = rel_path.replace("\\","/").split("/")
	verified_path_elements = [ ] 
	
	for elem in rel_path_elements:
		dir_map = {f.lower(): f for f in os.listdir(normalized_root_path + "/" + "/".join(verified_path_elements))}	
		if elem.lower() not in dir_map:
			return rel_path, False
		verified_path_elements.append(dir_map[elem.lower()])
		
	return "/".join(verified_path_elements), True
	
	
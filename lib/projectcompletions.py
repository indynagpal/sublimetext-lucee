import os, threading, sublime, time
from .componentfinder import load_directory, load_file, get_bean_names
from functools import partial

projects = {}
lock = threading.Lock()

def sync_projects(project_list):
	global projects
	with lock:
		current_project_names = set(projects.keys())
		updated_project_names = {project_name for project_name, project_data in project_list}
		#print(current_project_names,updated_project_names)
		new_project_names = list(updated_project_names.difference(current_project_names))
		stale_project_names = list(current_project_names.difference(updated_project_names))
		#print(new_project_names,stale_project_names)
		# remove stale projects
		for project_name in stale_project_names:
			del projects[project_name]
		# add new projects
		for project_name, project_data in project_list:
			if project_name in new_project_names:
				projects[project_name] = {"project_data": project_data, "completions": {}}
	# now that projects dict is up to date release lock before initing directory load
	for project_name, project_data in project_list:
		if project_name in new_project_names:
			load_project_async(project_name, project_data)

def load_project_async(project_name, project_data):
	sublime.set_timeout_async(partial(load_project, project_name, project_data))

def load_project(project_name, project_data):
	model_completion_folders = project_data.get("model_completion_folders", [])
	if len(model_completion_folders) == 0:
		return

	start_time = time.clock()
	file_count = 0
	project_completions = {}
	print("Lucee: indexing project '" + project_name + "'" )

	for path in model_completion_folders:
		# normalize path
		path = path.replace("\\","/")
		if path[-1] != "/":
			path = path + "/"
		completions, count = load_directory(path)
		project_completions.update(completions)
		file_count += count
	projects[project_name] = {"project_data": project_data, "completions": project_completions}
	print("Lucee: indexing project '" + project_name + "' completed - " + str(file_count) + " files indexed in " + "{0:.2f}".format(time.clock() - start_time) + " seconds")

def load_project_file(project_name, project_data, file_path, bean_names=None):
	# check for tracked file path
	model_completion_folders = project_data.get("model_completion_folders", [])
	for root_path in model_completion_folders:
		# normalize root_path
		root_path = root_path.replace("\\","/")
		if root_path[-1] != "/":
			root_path = root_path + "/"
		if file_path.replace("\\","/").startswith(root_path):
			# check for bean names
			if not bean_names:
				bean_names = get_bean_names(root_path, file_path)
			file_completions = load_file(file_path, bean_names)
			# lock for setting file completions
			with lock:
				if project_name not in projects:
					projects[project_name] = {"project_data": project_data, "completions": project_completions}
				projects[project_name]["completions"].update(file_completions)

def has_completions(project_name, bean_name):
	if project_name in projects:
		return bean_name.lower() in projects[project_name]["completions"]
	return False

def get_completions(project_name, bean_name):
	return projects[project_name]["completions"][bean_name.lower()]
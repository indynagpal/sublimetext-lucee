from .projectcompletions import get_dot_completions, load_project_file, sync_projects
from .. import events, completions

def plugin_loaded():
	sync_projects()

def on_post_save_async(view):
	if view.window().project_file_name():
		load_project_file(view.window().project_file_name(), view.window().project_data(), view.file_name())

events.subscribe('on_load_async', lambda view: sync_projects())
events.subscribe('on_close', lambda view: sync_projects())
events.subscribe('on_post_save_async', on_post_save_async)

completions.add_completion_source('dot', get_dot_completions)
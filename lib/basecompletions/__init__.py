from .. import completions
from . import basecompletions

basecompletions.load_completions()
completions.add_completion_source('tag', basecompletions.get_tags)
completions.add_completion_source('tag_attributes', basecompletions.get_tag_attributes)
completions.add_completion_source('script', basecompletions.get_script_completions)
completions.add_completion_source('dot', basecompletions.get_member_functions)

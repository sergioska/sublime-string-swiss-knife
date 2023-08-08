import sublime
import sublime_plugin


class PrefixCommandInputHandler(sublime_plugin.TextInputHandler):
	def initial_text(self):
		return "ls -al"

class SuffixCommandInputHandler(sublime_plugin.TextInputHandler):
	def initial_text(self):
		return "ls -al"
class EndCommandPatternInputHandler(sublime_plugin.TextInputHandler):
	def initial_text(self):
		return "\n\n"

class TargetPatternInputHandler(sublime_plugin.TextInputHandler):
	def initial_text(self):
		return "\n"

class ReplacePatternInputHandler(sublime_plugin.TextInputHandler):
	def initial_text(self):
		return ","

class ChunkizeTargetPatternInputHandler(sublime_plugin.TextInputHandler):
	def initial_text(self):
		return ","

class ChunkizeReplacePatternInputHandler(sublime_plugin.TextInputHandler):
	def initial_text(self):
		return "\n\n"

class ChunkizeSizeInputHandler(sublime_plugin.TextInputHandler):
	def initial_text(self):
		return 1000

class ChunkizeCommand(sublime_plugin.TextCommand):
	def run(self, edit, chunkize_target_pattern, chunkize_replace_pattern, chunkize_size):
		whole_region = sublime.Region(0, self.view.size())
		text = self.view.substr(sublime.Region(0, self.view.size()))
		items = text.split(chunkize_target_pattern)
		chunkedItems = self.split_list(items, int(chunkize_size))
		print(chunkedItems)
		output = '';
		for chunk in chunkedItems:
			group = chunkize_target_pattern.join(map(str, chunk))
			output = output + group + chunkize_replace_pattern
		self.view.replace(edit, whole_region, output)
	def input(self, args):
		if 'chunkize_target_pattern' not in args:
			return ChunkizeTargetPatternInputHandler()
		if 'chunkize_replace_pattern' not in args:
			return ChunkizeReplacePatternInputHandler()
		if 'chunkize_size' not in args:
			return ChunkizeSizeInputHandler()
	def split_list(self, lst, chunk_size):
		for i in range(0, len(lst), chunk_size):
			yield lst[i:i+chunk_size]

class JoinizeCommand(sublime_plugin.TextCommand):
	def run(self, edit, target_pattern, replace_pattern):
		print(target_pattern)
		print(replace_pattern)
		whole_region = sublime.Region(0, self.view.size())
		text = self.view.substr(sublime.Region(0, self.view.size()))
		output = text.replace(target_pattern, replace_pattern)
		self.view.replace(edit, whole_region, output)
	def input(self, args):
		if 'target_pattern' not in args:
			return TargetPatternInputHandler()
		if 'replace_pattern' not in args:
			return ReplacePatternInputHandler()

class ScriptizeCommand(sublime_plugin.TextCommand):
	def run(self, edit, prefix_command, suffix_command, end_command_pattern):
		whole_region = sublime.Region(0, self.view.size())
		text = self.view.substr(sublime.Region(0, self.view.size()))
		text = prefix_command + text
		output = text.replace(end_command_pattern, suffix_command)
		self.view.replace(edit, whole_region, output)
	def input(self, args):
		if 'prefix_command' not in args:
			return PrefixCommandInputHandler()
		if 'suffix_command' not in args:
			return SuffixCommandInputHandler()
		if 'end_command_pattern' not in args:
			return EndCommandPatternInputHandler()


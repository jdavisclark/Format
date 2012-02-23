import jsbeautifier

class JsFormatter():
	def __init__(self, settings):		
		self.settings = settings

	def name(self):
		return "javascript formatter"

	def accept(self, ext, syntax):
		acc = False
		if(ext != None):
			acc = ext == "js"
		if(acc == False and syntax != None):
			acc = syntax.find("javascript") != -1
		
		return acc

	def format(self, s, view):
		vSettings = view.settings()

		# settings
		opts = jsbeautifier.default_options()
		opts.indent_char = " " if vSettings.get("translate_tabs_to_spaces") else "\t"
		opts.indent_size = int(vSettings.get("tab_size")) if opts.indent_char == " " else 1 
		opts.max_preserve_newlines = self.settings.get("max_preserve_newlines") or 3
		opts.preserve_newlines = self.settings.get("preserve_newlines") or True
		opts.jslint_happy = self.settings.get("jslint_happy") or False
		opts.brace_style = self.settings.get("brace_style") or "collapse"
		opts.keep_array_indentation = self.settings.get("keep_array_indentation") or False
		opts.indent_level = self.settings.get("indent_level") or 0

		return jsbeautifier.beautify(s, opts)		
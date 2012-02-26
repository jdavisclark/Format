import sublime, sublime_plugin, re, os
from HtmlFormatter import HtmlFormatter
from JsFormatter import JsFormatter

formatSettings = sublime.load_settings('Format.sublime-settings')
jsSettings = sublime.load_settings('Format-Javascript.sublime-settings')
htmlSettings = sublime.load_settings('Format-Html.sublime-settings')

formatters = [JsFormatter(jsSettings), HtmlFormatter(htmlSettings)]

class FormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		fileRegion = sublime.Region(0, self.view.size())
		settings = self.view.settings()
		selection = self.view.sel()[0]

		# calculate pre-format non-whitespace offset
		nwsOffset = self.precedingNonWhitespace()		

		
		fName = self.view.file_name()		
		vSettings = self.view.settings()
		syntaxPath = vSettings.get('syntax')
		syntax = None
		ext = None

		if (fName != None): # file exists, pull syntax type from extension
			ext = os.path.splitext(fName)[1][1:]
		if(syntaxPath != None):
			syntax = os.path.splitext(syntaxPath)[0].split('/')[-1].lower()

		formatter = None

		for f in formatters:
			if (f.accept(ext, syntax) == True):
				formatter = f
				break


		if(formatter == None):
			sublime.status_message('Format: file/syntax type not currently supported!')
			return

		print 'Formatter Name: ' + formatter.name()

		# do formatting and replacement
		replaceRegion = selection if len(selection) > 0 else fileRegion

		formatted = formatter.format(self.view.substr(replaceRegion), self.view)
		self.view.replace(edit, replaceRegion, formatted)


		# re-place cursor
		offset = self.nwsOffset(nwsOffset, self.view.substr(fileRegion))
		rc = self.view.rowcol(offset)
		pt = self.view.text_point(rc[0], rc[1])
		sel = self.view.sel()
		sel.clear()
		self.view.sel().add(sublime.Region(pt))

		# make sure the 
		self.view.show_at_center(pt)


	def precedingNonWhitespace(self):
		pos = self.view.sel()[0].a
		preTxt = self.view.substr(sublime.Region(0, pos));
		return len(re.findall('\S', preTxt))

	def nwsOffset(self, nonWsChars, buff):
		nonWsSeen = 0
		offset = 0
		for i in range(0, len(buff)):
			offset += 1
			if not(buff[i].isspace()):
				nonWsSeen += 1
			
			if(nonWsSeen == nonWsChars):
				break

		return offset
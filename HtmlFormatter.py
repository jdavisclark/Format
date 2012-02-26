from BeautifulSoup import BeautifulSoup as bs

class HtmlFormatter:
	def __init__(self, settings):		
		self.settings = settings

	def name(self):
		return "html formatter"

	def format(self, s, view):
		soup = bs(s, indentWidth = self.settings.get("indent_string"))
		return soup.prettify()

	
	def accept(self, ext, syntax):
		acc = False
		if(ext != None) :
			acc = ext in ["html", "asp", "aspx", "mustache", "htm", "xml"]
		if(acc == False and syntax != None):
			acc = syntax.find("html") != -1
		
		return acc

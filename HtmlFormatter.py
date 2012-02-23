from BeautifulSoup import BeautifulSoup as bs

class HtmlFormatter:
	def __init__(self, settings):		
		self.settings = settings

	def name(self):
		return "html formatter"

	def format(self, s, view):
		soup = bs(s, indentWidth = "    ")
		return soup.prettify()

	
	def accept(self, ext, syntax):
		if(ext != None) :
			return ext == "html"
		elif(syntax != None):
			return syntax.find("html") != -1
		else:
			return False
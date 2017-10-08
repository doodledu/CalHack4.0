from lxml import html
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ProfessorCrawler:

	def __init__(self, starting_url, depth):
		self.starting_url = starting_url
		self.depth = depth
		self.professors = []

	def crawl(self):
		self.get_professor_from_link(self.starting_url)
		return

	def get_professor_from_link(self, link):
		start_page = requests.get(link)
		text_file = open("Output.txt", "w")
		text_file.write(start_page.text)
		text_file.close()
		tree = html.fromstring(start_page.text)
		print(start_page)
		professorList = tree.xpath('//div[@class="side-panel"]/div[@class="result-list"]/ul')

		print(professorList)


		'''
		firstname = tree.xpath('//h1[@class="profname"]/span[@class="pfname"]/text()')[0].strip()
		lastname = tree.xpath('//h1[@class="profname"]/span[@class="plname"]/text()')[0].strip()
		quality = tree.xpath('//div[@class="grade"]/text()')[0].strip()
		difficulty = tree.xpath('//div[@class="grade"]/text()')[2].strip()
		'''
		#links = tree.xpath('//div[@class="center-stack"]//*/a[@class="name"]/@href')
		'''
		professor = Professor(firstname, lastname, quality, difficulty)
		self.professors.append(professor)'''

class Professor:

	def __init__(self, firstname, lastname, quality, difficulty):
		self.firstname = firstname
		self.lastname = lastname
		self.quality = quality
		self.difficulty = difficulty

	def __str__(self):
		return ("Name: "+ self.firstname+ " "+ self.lastname+
			"\r\nQuality: "+self.quality+
			"\r\nDifficulty: " + self.difficulty +"\r\n")

crawler = ProfessorCrawler('http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+California+Berkeley&schoolID=1072&queryoption=TEACHER', 0)
crawler.crawl()

for professor in crawler.professors:
	print professor
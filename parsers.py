import feedparser as fp
import requests
from bs4 import BeautifulSoup as bs

class CnnParser:

	def __init__(self) -> None:
		cnn_feed = 'http://rss.cnn.com/rss/cnn_allpolitics.rss'
		# parse all from the politics feed
		cnn_politics = fp.parse(cnn_feed)
		self.entries = cnn_politics.entries
	
	def getTitles(self) -> list:
		return [entry['title'] for entry in self.entries]
		
	def getEntries(self):
		return self.entries

	def getSummaries(self):
		return [entry['value'] for entry in self.entries]

	def getArticle(self, link_to_article):
		data = requests.get(link_to_article)

		soup = bs(data.text, 'html.parser')
		p_tags = soup.find_all('div', class_="zn-body__paragraph")
		
		content = [tag.text for tag in p_tags]
		return '\n'.join(content)
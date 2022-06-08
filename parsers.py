import feedparser as fp
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

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

	def getContent(self, link_to_article):
		data = requests.get(link_to_article)

		soup = bs(data.text, 'html.parser')
		p_tags = soup.find_all('div', class_="zn-body__paragraph")
		
		content = [tag.text for tag in p_tags]
		return '\n'.join(content)

	def getLinks(self):
		return [entry['id'] for entry in self.entries]

	def getAuthors(self, link_to_article):
		data = requests.get(link_to_article)

		soup = bs(data.text, 'html.parser')
		tag = soup.find('span', class_='metadata__byline__author')

		return tag.text

	# for every article get the required data and return a list of dicts
	def parse(self):
		data = []
		for entry in self.entries:
			title = entry['title']
			summary = entry['summary']
			archive_date = datetime.now()
			authors = None # need to add
			orig_article_link = entry['id']
			content = self.getContent(orig_article_link)

			dict = {
				'title': title,
				'summary': summary,
				'archive_date': archive_date,
				'authors': authors,
				'orig_article_link': orig_article_link,
				'content': content,
				'source': 'CNN'
			}
			data.append(dict)
		return data

test = CnnParser()
entries = test.entries

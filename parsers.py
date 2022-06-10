import dataclasses
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
		#self.filter()

	def getTitle(self, entry):
		return entry['title']

	def getSummary(self, entry):
		text = entry['summary']
		tag_start = text.index('<')
		return text[0:tag_start]
	
	def getArchiveDate(self):
		return datetime.now()

	def getOrigArticleUrl(self, entry):
		return entry['link']

	def getContent(self, entry):
		data = requests.get(self.getOrigArticleUrl(entry))

		soup = bs(data.text, 'html.parser')
		p_tags = soup.find_all('div', class_="zn-body__paragraph")
		
		content = [tag.text for tag in p_tags]
		return '\n'.join(content)

	def getPublishedDate(self, entry):
		if 'published' in entry:
			return entry['published']
		return self.getArchiveDate().strftime('%d %M %Y')

	def getAuthors(self, entry):
		data = requests.get(self.getOrigArticleUrl(entry))

		soup = bs(data.text, 'html.parser')
		tag = soup.find('span', class_='metadata__byline__author')

		if tag:
			return tag.text

	def getImageUrl(self, entry):
		if 'media_content' in entry:
			images = entry['media_content']
			if not images:
				return 
			if images[0]['medium'] == 'image':
				return images[0]['url']
		return ' '

	# for every article get the required data and return a list of dicts
	def parse(self):
		data = []
		for entry in self.entries:
			dict = {
				'title': self.getTitle(entry),
				'summary': self.getSummary(entry),
				'archive_date': self.getArchiveDate(),
				'authors': self.getAuthors(entry),
				'orig_article_link': self.getOrigArticleUrl(entry),
				'content': self.getContent(entry),
				'source': 'CNN',
				'published_date': self.getPublishedDate(entry),
				'image_url': self.getImageUrl(entry)
			}
			data.append(dict)
		return data

class NprParser:

	def __init__(self) -> None:
		npr_feed = 'https://feeds.npr.org/1001/rss.xml'
		# parse all from the politics feed
		npr_politics = fp.parse(npr_feed)
		self.entries = npr_politics.entries
		#self.filter()

	def filter(self):
		valid_keys = {
			'title',
			'summary',
			'id',
			'media_content',
			'author',
			#'published'
		}

		for entry in self.entries[:]:
			if not valid_keys.issubset(set(entry.keys())):
				self.entries.remove(entry)

	def getContent(self, link_to_article):
		data = requests.get(link_to_article)

		soup = bs(data.text, 'html.parser')
		p_tags = soup.find_all('div', id="storytext")
		
		content = [tag.text for tag in p_tags]
		return '\n'.join(content)

	def getAuthors(self, link_to_article):
		data = requests.get(link_to_article)

		soup = bs(data.text, 'html.parser')
		tags = soup.find_all('p', class_='byline__name byline__name--block')

		content = [tag.text.strip() for tag in tags]
		return ' '.join(content)

	def getImageUrl(self, entry):
		content = entry['content']
		if not content:
			return
		
		value = content[0]['value']
		src_index = value.index('src=')
		closed_index = value.find('/>')
		url = value[src_index + 4: closed_index]
		return url

	def parse(self):
		data = []
		for entry in self.entries:
			dict = {
				'title': entry['title'],
				'summary': entry['summary'],
				'archive_date': datetime.now(),
				'authors': entry['author'],
				'orig_article_link': entry['id'], # confirm
				'content': self.getContent(),
				'source': 'NPR',
				'published_date': entry['published'],
				'image_url': self.getImageUrl()
			}
			data.append(dict)

		return data
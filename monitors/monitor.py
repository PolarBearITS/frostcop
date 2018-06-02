import requests
import threading
from bs4 import BeautifulSoup as bsoup
from requests_futures.sessions import FuturesSession
class monitor:
	def __init__(self):
		self.needsSoup

	def refresh(self):
		pass

	def check_stock(self):
		raise NotImplementedError("check_stock must be defined in child monitor class.")

	def scrape(self):
		n = len(self.links)
		if n < 0:
			n = 1
		session = FuturesSession(max_workers=n)
		reqs = ()
		for link in self.links:
			reqs += (session.get(link),)
		self.responses = [r.result() for r in reqs]
		if self.needsSoup:
			pass

		
	def make_soup(self, response):
		return bsoup(response.content, 'html.parser')

	def run(self):
		print(self.url)
		print(self.needsSoup)
		self.refresh()
		self.scrape()
		for resp in self.responses:
			pass

class soup:
	def __init__(self, link):
		self.response = requests.get(link)
		self.soup = bsoup(self.response.content, 'html.parser')

class request:
	def __init__(self, link):
		self.response = requests.get(link)
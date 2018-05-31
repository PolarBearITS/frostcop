import requests
from bs4 import BeautifulSoup as bsoup
class monitor:
	def __init__(self):
		pass

	def refresh(self):
		pass

	def check_stock(self):
		raise NotImplementedError("check_stock must be defined in child monitor class.")

	def run(self):
		print(self.url)
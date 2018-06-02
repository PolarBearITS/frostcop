from .. import monitor
class supreme(monitor.monitor):
	url = 'http://www.supremenewyork.com'
	needsSoup = True

	def refresh(self):
		self.links = []
		home = monitor.soup(self.url + '/shop/all')
		for div in home.soup.find_all('div', {'class': 'inner-article'}):
			self.links.append(self.url + div.find('a')['href'])

	def check_stock(self, page):
		pass
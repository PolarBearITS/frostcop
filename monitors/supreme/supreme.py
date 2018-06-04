from .. import monitor
class supreme(monitor.monitor):
	url = 'http://www.supremenewyork.com'
	needs_soup = True

	def refresh(self):
		self.links = []
		home = monitor.soup(self.url + '/shop/all')
		for div in home.soup.find_all('div', {'class': 'inner-article'}):
			self.links.append(self.url + div.find('a')['href'])

	def check_stock(self, page_index):
		page = self.soups[page_index]
		name = page.find('h1', {'class': 'protect'}).text
		color = page.find('p', {'class': 'protect'}).text
		stock = bool(page.find('fieldset', {'id': 'add-remove-buttons'}).find('input'))
		print(name, color, stock)
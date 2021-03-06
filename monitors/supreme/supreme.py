from .. import monitor
class supreme(monitor.monitor):
	url = 'http://www.supremenewyork.com'
	needs_soup = True
	webhook = 'https://discordapp.com/api/webhooks/435954570292756480/fLbreq3dFc_afDOZqtXYnDWDcgpc0mF-RKtUF55vXLKOej4sXCaHJx2Ac7IyzHVpw0hM'

	def refresh(self):
		self.links = []
		home = self.request(self.url + '/shop/all')
		print(home)
		for div in self.soupify(home).find_all('div', {'class': 'inner-article'}):
			link = self.url + div.find('a')['href']
			self.links.append(link)

	def check(self, page_index):
		page = self.soups[page_index]
		name = page.find('h1', {'itemprop': 'name'}).text
		color = page.find('p', {'itemprop': 'model'}).text
		price = page.find('span', {'itemprop': 'price'}).text
		select = page.find('select', {'name': 's'})
		sizes = []
		if select:
			sizes = [option.text for option in select.find_all('option')]
		print(sizes)
		stock = bool(page.find('fieldset', {'id': 'add-remove-buttons'}).find('input'))
		prod = monitor.product(self.links[page_index], name, price, stock, variant=color, sizes=sizes)
		self.update(prod)
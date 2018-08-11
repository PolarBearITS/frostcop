from .. import monitor
import re
class snkrs(monitor.monitor):
	url = 'https://www.nike.com'
	needs_soup = True
	webhook = 'https://discordapp.com/api/webhooks/435954570292756480/fLbreq3dFc_afDOZqtXYnDWDcgpc0mF-RKtUF55vXLKOej4sXCaHJx2Ac7IyzHVpw0hM'

	def refresh(self):
		print('refreshing')
		self.links = []
		home = self.request(self.url + '/launch/?s=in-stock')
		print('getting links')
		# print(home.content.decode('utf-8'))
		h = home.content.decode('utf-8')
		pair = []
		for i, l in enumerate(re.finditer('figure', h)):
			print(i, l)
		for i, l in enumerate(re.finditer('figure', h)):
			if i % 2 == 0:
				print(pair)
				pair = []
			pair.append(l)
		print(pair)
		# x = self.soupify(home)
		print('souped')
		quit()
		for figure in x.find_all('figure'):
			link = self.url + figure.find('a')['href']
			# print(link)
			self.links.append(link)
		# quit()
		# print(self.links)
from .. import monitor
import re
class snkrs(monitor.monitor):
	url = 'https://www.nike.com'
	webhook = 'https://discordapp.com/api/webhooks/435954570292756480/fLbreq3dFc_afDOZqtXYnDWDcgpc0mF-RKtUF55vXLKOej4sXCaHJx2Ac7IyzHVpw0hM'

	def refresh(self):
		self.links = []
		home = self.request(self.url + '/launch/?s=in-stock')
		print()
		# print(home.content.decode('utf-8'))
		h = home.content.decode('utf-8')
		r = re.finditer('<figure .+?href="(.+?)".+?<\/figure>', h)
		for l in r:
			self.links.append(self.url + l.group(1))
		print(self.links)
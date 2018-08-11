import pickle
import requests
import threading
from bs4 import BeautifulSoup as bsoup
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed

class proxy:
	def __init__(self, ip, port, region):
		self.ip = ip
		self.port = port
		self.region = region
		self.proxy = {
			'http': f'http://{self.ip}:{self.port}'
		}

	def connect(self, url):
		print(self)
		try:
			r = requests.get(url, proxies=self.proxy, timeout=5)
			# if r.status_code == 200:
			# 	return True
			print(r, requests.status_codes._codes[r.status_code][0])
		except (KeyboardInterrupt, SystemExit):
			print('Interrupted by user.')
			quit()
		except Exception as e:
			print(e)
		# return False
	def __str__(self):
		# return str({'ip': self.ip, 'port': self.port, 'region': self.region})
		return str((self.ip, self.port, self.region))


sites = ['http://supremenewyork.com', 'http://www.adidas.com']

url = 'https://www.us-proxy.org/'
soup = bsoup(requests.get(url).content, 'lxml')
table = soup.find('tbody')
keys = [th.text for th in soup.find('thead').find('tr').find_all('th')]
candidates = []
for tr in table.find_all('tr'):
	vals = [td.text for td in tr.find_all('td')]
	d = dict(zip(keys, vals))
	if d['Anonymity'] == 'elite proxy':
		candidates.append(d)
proxies = []

for c in candidates:
	p = proxy(c['IP Address'], c['Port'], c['Code'])
	if p.connect(sites[1]):
		print(p)
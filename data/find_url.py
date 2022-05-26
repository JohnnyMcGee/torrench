'''
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>

This file is part of Torrench.

Torrench is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Torrench is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>. 
'''

from bs4 import BeautifulSoup
import requests

proxy_list_url = 'https://piratebayproxy.info/'

def _url_is_ok(url: str):
	try:
		res = requests.get(url)
		return res.ok
	except Exception as e:
		print(e)

def find_proxy_url() -> str:
	raw = requests.get(proxy_list_url)
	soup = BeautifulSoup(raw.content, "lxml")
	links = [s['href'] for s in soup.find_all('a', class_='t1')]
	for lnk in links:
		if _url_is_ok(lnk):
			return lnk

if __name__ == "__main__":
	print("It's a module. Can only be imported!")

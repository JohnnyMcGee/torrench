'''
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>

This file is part of Torrench.

Torrench is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Torrench is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>. 
'''

from bs4 import BeautifulSoup
import requests

url = 'https://piratebayproxy.info/'
raw = requests.get(url)
raw = raw.content
soup = BeautifulSoup(raw, "lxml")
links = [s['href'] for s in soup.find_all('a', class_='t1')]
# links = soup.find_all('td', {'title': 'URL'}, limit=2)
def find_url_list():
	myList = []
	for lnk in links:
		myList.append(lnk);
	return myList

if __name__ == "__main__":
	print("It's a module. Can only be imported!");

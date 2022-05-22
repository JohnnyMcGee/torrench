import os
import requests
from bs4 import BeautifulSoup

class TorrentDetail:
    def __init__(self: 'TorrentDetail', url: str, index: any) -> 'Torrent':
        self.url = url
        self.index = index
        raw = requests.get(url);
        self.raw = raw.content
        self.unique_id = self.url.split('/')[-1]
        self.file_name = self.unique_id+".html"

        soup = BeautifulSoup(self.raw, "lxml")
        
        content = soup.find('div', id="details")
        self.content = content
        self.nfo = str(content.find_all('div', class_="nfo")[0])
        self.dt = content.find_all('dt')
        self.dd = content.find_all('dd')
        title = soup.find('div', id="title")
        self.title = "(Index: "+self.index+") - "+str(title.string)
        self.name = str(soup.find('div', id="title"))
        self.magnet = soup.find('div', class_="download").a["href"]
        self.comment = soup.find_all('div', class_='comment')
        self.commenter = soup.find(id="comments").find_all('p')
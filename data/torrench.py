#! /usr/bin/python3

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

import os
import subprocess
import sys
import argparse
import urllib
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from scrape_option import scrape_option
import pandas as pd

from find_url import find_proxy_url
from TorrentDetail import TorrentDetail

def init(args: argparse.Namespace) -> None:
    title = urllib.parse.quote(' '.join(args.search))
    page_limit = args.limit
    if args.clear_html:
        home = os.path.expanduser('~')
        temp_dir = home+"/.torrench/temp/"
        files = os.listdir(temp_dir)
        if not files:
            print("\nNothing to remove\n")
        else:
            count = 0
            for i in files:
                os.remove(os.path.join(temp_dir, i))
                count = count+1
            print("\nRemoved %d file(s).\n" % count)
        sys.exit()
    if len(title) == 0:
        print("\nSearch string expected.\nUse --help for more\n")
        sys.exit()
    elif page_limit <= 0 or page_limit > 50:
        print("Enter valid page input [0<pg<=50]")
        sys.exit()
    elif not os.path.isdir(args.directory):
        print("Invalid directory. Please try again")
        sys.exit()
    else:
        main(title, page_limit, category=args.category, args=args)

def main(title: str, page_limit: int, category: int, args:argparse.Namespace) -> None:
    df = pd.DataFrame(columns=["category","sub_category","name","seeds","leeches","size","date","uploader","comment","page","link"])
    url = find_proxy_url()

    for pg in range(page_limit):
        if page_limit > 1:
            fetch_status_str = "\nFetching from page: "+str(pg+1)
        else:
            fetch_status_str = "\n(Optional) Use [-p] option to specify pages.\n\nFetching results (Max: 30)...\n(Might take longer. Be patient)"
        print(fetch_status_str)

        # confirm there is data on the page
        search_url = f"{url}/search/{title}/{pg+1}/99/{category}"
        raw = requests.get(search_url)
        soup = BeautifulSoup(raw.content, "lxml")
        table = soup.table
        if not table or len(table.find_all('tr')) < 3:
            if pg == 0:
                print("\nNo results found for given input!")
            break
        rows = table.find_all('tr')[1:-1]

        # scrape options into dataframe
        for row in rows:
            option = scrape_option(row)
            option["page"]=pg+1
            df.loc[len(df.index)+1]=option
            
        num_results_in_page=len(df[df["page"] == pg+1])
        print(f">> {num_results_in_page} torrents")

    # Print Results and fetch torrent details
    result_count = len(df)
    page_count = df.page.nunique()
    if result_count > 0:
        df["categ"] = df["category"] + df["sub_category"]
        mini_df = df[["categ","name","seeds","leeches","size"]]
        mini_df = mini_df.rename(mapper={"categ":"category"}, axis="columns")
        mini_df.columns=[c.title() for c in mini_df.columns]
        while True:
            print(tabulate(mini_df, headers='keys', tablefmt='grid'))
            print(f"\nTotal: {result_count} torrents")
            print(f"Total pages: {page_count}")
            print("\nFurther, a torrent's details can be fetched (Description, comments, download(Magnetic) Link, etc.)")
            print("Enter torrent's index value to fetch details (Maximum one index)\n")

            option = input("(0 = exit)\nindex > ")
            if option.isdigit():
                option=int(option)
            else:
                print("**Enter valid index**\n\n")
                continue
            if option > result_count or option < 0 or option == "":
                print("**Enter valid index**\n\n")
                continue
            elif option == 0:
                break
            else:
                t = TorrentDetail(df.loc[option].link, df.loc[option].name)
                _handle_selection(t, args)
        print("\nDone")

def _handle_selection(t: TorrentDetail, args: argparse.Namespace) -> None:
    def _display_details(t: TorrentDetail) -> None:
        print(t.title)
        for d in list(zip(t.dt,t.dd)):
            if d[0]:
                print(d[0].get_text().strip(), d[1].get_text().replace('\n', ' '))
        print(t.nfo) 
                        
    def _launch_rtorrent(t: TorrentDetail) -> None:
        try:
            subprocess.call(['rtorrent','-d', args.directory, t.magnet])
        except Exception as e:
            print("Error: ", e)
            print ('Rtorrent does not exist. Please install and try again.')   
    
    def _save_as_html(t: TorrentDetail):
        from details import save_as_html
        print(f"Fetching details for torrent: {t.title}")
        file_url = save_as_html(t)
        print("\nFile URL: "+file_url+"\n\n")
    
    def _display_magnet(t: TorrentDetail) -> None:
        print(t.magnet)
    
    if args.html:
        _save_as_html(t)
    if args.info:
        _display_details(t)
    if args.magnet:
        _display_magnet(t)
    if args.rtorrent:
        _launch_rtorrent(t)
    # DEFAULT
    if not any([args.html, args.info, args.magnet, args.rtorrent]):
        actions = {"i":_display_details, "m": _display_magnet, "r": _launch_rtorrent, "h": _save_as_html}
        while True:
            print(f"Choose an action for {t.title}")
            print("i => info | ","m => magnet | ","r => launch rtorrent | ","h => save as html | ", "b => back")
            res = input("(0 = exit) action > ").lower()
            if res=="0":
                sys.exit()
            elif res=="b":
                break
            elif res in actions:
                actions[res](t)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A simple torrent search tool.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("search", help="Enter search string",
                        nargs="*", default=None)
    parser.add_argument("-p", "--page-limit", type=int,
                        help="Number of pages to fetch results from (1 page = 30 results).\n [default: 1]", default=1, dest="limit")
    parser.add_argument("--clear-html", action="store_true", default=False,
                        help="Clear all torrent description HTML files and exit.")
    parser.add_argument("-v", "--version", action='version',
                        version='%(prog)s v1.0', help="Display version and exit.")
    parser.add_argument("-c", "--category", default=0,
                        help="number corresponding to the category of search (0=all 207=HD Movies 208=HD TV Shows)")
    parser.add_argument("-m", "--magnet", action="store_true",
                        default=False, help="print out magnet links")
    parser.add_argument("-rt", "--rtorrent", action="store_true",
                        default=False, help="open magnet link in rtorrent")
    parser.add_argument("-d", "--directory", action="store",
                        default=os.path.expanduser('./'), help="location to store downloads")
    parser.add_argument("--info", action="store_true",
                        default=False, help="print info about the torrent")
    parser.add_argument("--html", action="store_true",
                        default=False, help="save details to html")
    args = parser.parse_args()
    init(args)

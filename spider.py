#!usr/bin/env/python

import requests
import re
from urllib.parse import *

target_url = "https://root_directory/"
target_links = []

def get_links(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))


def crawl(url):
    href_links = get_links(url)
    for link in href_links:
        # link = urlparse(link)
        # link = f"{link.scheme}://{link.netloc}{link.path}"
        link = urljoin(url, link)
        if "#" in link:
            link = link.split('#')[0]
        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            # recursively searches fpr new links
            crawl(link)


crawl(target_url)
#!/usr/bin/env python

import requests
import re
from urllib.parse import urljoin
import sys


if len(sys.argv) < 2:
    print("Usage: python script.py <target_url>")
    sys.exit(1)

target_url = "https://" + sys.argv[1]
target_links = []
MAX_DEPTH = 3  # Limit recursion depth

def get_links(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)
        return re.findall(r'href=["\'](.*?)["\']', response.text)
    except requests.RequestException as e:
        print(f"[-] Error fetching {url}: {e}")
        return []

def crawl(url, depth=0):
    if depth > MAX_DEPTH:
        return

    href_links = get_links(url)
    for link in href_links:
        link = urljoin(url, link)
        if "#" in link:
            link = link.split('#')[0]
        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link, depth + 1)  # Increment depth

crawl(target_url)

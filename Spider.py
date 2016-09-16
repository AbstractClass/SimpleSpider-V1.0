import requests
from bs4 import BeautifulSoup
from urllib import parse
import re

__author__ = 'Connor MacLeod'


def fetch_page(url):  # Gets the page with requests module
    return requests.get(url)


def clean_links(parent_url, dirty_links):  # Removes same-page links and fixes partial links
    separators = ['?', '#']
    cleaned = set()
    for link in dirty_links:
        for sep in separators:
            link = link.split(sep, 1)[0]

        if 'http://' not in link:
            link = parse.urljoin(parent_url, link)

        cleaned.add(link)

    return cleaned


def find_links(soup):  # Will be expanded to utilise different methods (ghost.py, twisted, raw lxml, etc.)
    links_in_html = (link['href'] for link in soup.find_all('a', href=True))

    return links_in_html


def found_in_soup(search_string, soup):
    if soup.body.findAll(text=search_string):
        return True
    else:
        return False


def log_info(title, info, outfile=None):  # If no outfile is provided, will save each page under the name of it's url
    if outfile:
        log_location = outfile
    else:
        log_location = re.sub('[/\\:*"?]', '_', title)
    with open(log_location, 'a', encoding='utf-8') as log:
        log.write('***\n' + title + '\n' + info + '\n')


def spider(base_url, max_pages=None, halt_phrase=None, cache_pages=False, outfile=None):
    queued_links = {base_url}
    new_links = set()
    seen_links = set()
    found_phrase = False

    if max_pages:
        countdown = max_pages
    else:
        countdown = -1

    while countdown != 0 and not found_phrase:
        for url in queued_links:
            webpage = fetch_page(url)
            html = webpage.text
            soup = BeautifulSoup(html, 'lxml')
            if cache_pages:
                log_info(url, html, outfile)

            if halt_phrase:
                found_phrase = found_in_soup(halt_phrase, soup)

            raw_links = find_links(soup)
            good_links = clean_links(url, raw_links)
            new_links = new_links | good_links

            print(url, "seen")
            print(len(new_links), " new links found")

            countdown -= 1
            if countdown == 0:
                print(max_pages, " pages seen, stopping spider...")
                break

        seen_links = seen_links | queued_links
        queued_links, new_links = new_links, set()  # Move new links to the queue, then reset new_links set


if __name__ == "__main__":
    spider('http://wikipedia.org/wiki/Spider', max_pages=10, cache_pages=True)
#    page = fetch_page('http://wikipedia.org/wiki/Spider')
#    soup = BeautifulSoup(page.text, 'lxml')
#    raw_links = find_links(soup)
#    good_links = clean_links(page.url, raw_links)
#    print(list(good_links))
#    print(found_in_soup('Spider', soup))
#    log_info(page.url, page.text, 'mylog.txt')

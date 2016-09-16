import requests
from bs4 import BeautifulSoup
from urllib import parse
import re
import time

__author__ = 'Connor MacLeod'


def fetch_page(url):  # Gets the page with requests module
    timeout = 50
    while timeout > 0:
        try:
            return requests.get(url)
        except Exception as e:
            print('requests is mad because: ', e, ' trying again in 5s.  Timeout in: ', timeout)
            timeout -= 1
            time.sleep(5)


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
    try:
        if soup.body.findAll(text=search_string):
            return True
        else:
            return False
    except Exception as e:
        print('page could not be read due to: ', type(e), e)
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

            links_last_round = len(new_links)

            raw_links = find_links(soup)
            good_links = clean_links(url, raw_links)
            new_links = new_links | good_links

            print(url, "scanned")
            print(len(new_links) - links_last_round, " new links found")
            countdown -= 1
            if countdown == 0:
                print(max_pages, " pages seen, stopping spider...")
                break

        seen_links = seen_links | queued_links
        queued_links, new_links = new_links, set()  # Move new links to the queue, then reset new_links set


if __name__ == "__main__":
    spider('http://Disney.com', max_pages=50, halt_phrase='Deadpool')

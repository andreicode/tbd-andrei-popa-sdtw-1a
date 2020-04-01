from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import time
import os

def store_page(url, path, pagedata):
    filepath = './data/' + url + path + '/page.data'
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc:
            print(exc)
    try:
        with open(filepath, 'w') as f:
            f.write(pagedata)
    except OSError as err:
        print(err)

def store_reference(url, path, reference_url):
    filepath = './data/' + url + path + '/page.reference'
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc:
            print(exc)
    try:
        with open(filepath, 'a+') as f:
            if not reference_url in f.read():
                f.write(reference_url.strip("\n\r ") + os.linesep)
    except OSError as err:
        print(err)

def queue_get(line_num):
    with open("./coada.txt") as queue:
        for i, line in enumerate(queue):
            if i == line_num - 1:
                return line.strip("\n\r ")

def queue_push(url):
    with open("./coada.txt", "a+") as queue:
        queue.write(os.linesep + url)


def is_page_visited(url):
    parsed_url = urlparse(url)
    filepath = './data/' + parsed_url.netloc + parsed_url.path + '/page.data'
    return os.path.exists(filepath)

# def can_scrape(b_url):
#     robots = requests.get(b_url + '/robots.txt')


def visit_url(url):
    try:
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, features="html.parser")
        base_url = urlparse(url)
        store_page(base_url.netloc, base_url.path, data)
        for link in soup.find_all('a'):
            new_url = link.get('href')
            parsed_url = urlparse(new_url)
            if parsed_url.scheme:
                queue_push(link.get('href'))
                store_reference(parsed_url.netloc, parsed_url.path, base_url.netloc + base_url.path)
                
    except requests.exceptions.RequestException as e:
        print(e)

def init():
    with open('./coada.txt', 'w+') as f:
        f.write('https://github.com/')

def run():
    line_num = 1
    processed_num = 1
    url = queue_get(line_num)
    while url:
        print(url, processed_num)
        if not is_page_visited(url):
            visit_url(url)
            processed_num += 1
        line_num+=1
        url = queue_get(line_num)
        time.sleep(1)

init()
run()
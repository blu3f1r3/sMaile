# -*-coding:utf-8 -*
import logging
import os
import re
import traceback
from multiprocessing.pool import Pool
from urllib.request import urlopen

from bs4 import BeautifulSoup, SoupStrainer
from tqdm import tqdm


def parse_mailbox(data):
    mxs = data.split(' ')
    result = [0] * 3

    if len(mxs) > 3:
        result[2] = mxs[-1]
        result[1] = mxs[-2]
        result[0] = ' '.join(mxs[:2])
    else:
        result = mxs
    return str(result[2]).replace('"', "")

    # return result[2].replace('"', '')


def is_online():
    try:
        urlopen('http://google.com', timeout=10)
        return True
    except:
        logging.error(traceback.format_exc())
        return False


def get_email_domain_name(email):
    match = re.search(r'[\w\.-]+@[\w\.-]+', email)
    if match:
        tmp = match.group(0).split('@')[1].split('.')
        if len(tmp) <= 2:
            return '.'.join(tmp[len(tmp) - 2:])
        return '.'.join(tmp[1:])
    return email


autoconfig_url = "https://autoconfig.thunderbird.net/v1.1/"
root_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(root_dir, 'xml')
if not os.path.exists(path):
    os.mkdir(path)


def update_worker(link):
    _new_file = os.path.join(path, link)
    response = urlopen(autoconfig_url + link)

    with open(_new_file, 'wb') as f:
        f.write(response.read())


def update_provider():
    _link_list = []
    response = urlopen(autoconfig_url)
    processes = 30

    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features='html.parser'):
        if link.has_attr('href'):
            if re.match(r'([a-zA-Z0-9.]+)([.][a-zA-Z0-9]{2,})', link['href']):
                _link_list.append(link['href'])

    with Pool(processes=processes) as p:
        with tqdm(total=len(_link_list), desc='Updating configs') as pbar:
            for i, _ in enumerate(p.imap_unordered(update_worker, _link_list)):
                pbar.update()

    print("Autoconfigs are now up-to-date!")

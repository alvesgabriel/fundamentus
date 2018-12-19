# -*- coding: utf-8 -*-
import logging
import os
import re

import requests
from bs4 import BeautifulSoup

BASE = 'http://www.fundamentus.com.br/'
DETAILS = 'detalhes.php'
DIR = 'assets'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def parse(url):
    response = requests.get(url)
    bsobj = BeautifulSoup(response.content, 'lxml')

    for a in bsobj.find_all('a', href=re.compile(r'detalhes\.php\?papel=(\w){4,}')):
        if a:
            parse_details(a.text.strip())


def parse_details(paper):
    logging.info(f'[PAPER]:\t[{paper}]')
    url = f'{BASE}balancos.php?papel={paper}&tipo=1'
    logging.info(f'[URL]:\t[{url}]')
    response = requests.get(url)
    sid = response.cookies.get('PHPSESSID')
    parse_balance(sid, paper)


def parse_balance(sid, paper):
    url = f'http://www.fundamentus.com.br/planilhas.php?SID={sid}'
    logging.info(f'[URL_SID]:\t[{url}]')
    response = requests.get(url)
    filename = f'bal_{paper}.zip'
    logging.info(f'[FILE]:\t[{filename}]\n')
    if response.text != 'Ativo nao encontrado':
        with open(os.path.join('..', DIR, filename), 'wb') as f:
            f.write(response.content)
            f.close()
    else:
        logging.error(f'{response.text} ({paper})\n')


def create_dir():
    dir_assets = os.path.join('..', DIR)
    if not os.path.isdir(dir_assets):
        os.mkdir(dir_assets)


if __name__ == "__main__":
    create_dir()
    parse(BASE + DETAILS)

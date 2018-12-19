# -*- coding: utf-8 -*-
import scrapy

from fundamentus_requests import create_dir, DIR
import os


class FundamentusSpider(scrapy.Spider):
    name = 'fundamentus'
    allowed_domains = ['www.fundamentus.com.br']
    start_urls = ['http://www.fundamentus.com.br/detalhes.php']
    base = 'http://www.fundamentus.com.br/'

    def parse(self, response):
        create_dir()
        for paper in response.css('tr.par a::text').extract():
            href = f'balancos.php?papel={paper}&tipo=1'
            yield response.follow(href, self.parse_details)

    def parse_details(self, response):
        cookies = self._cookie_to_dict(response.request.headers.get('Cookie'))
        sid = cookies.get('PHPSESSID')
        href = f'planilhas.php?SID={sid}'
        yield response.follow(href, self.parse_balance)

    def parse_balance(self, response):
        filename = response.headers.get("Content-Disposition").decode('utf-8').split('=')[-1]
        print(f'file: {filename}')
        with open(os.path.join('..', DIR, filename), 'wb') as f:
            f.write(response.body)
            f.close()

    def _cookie_to_dict(self, set_cookie):
        cookies = {}
        for attr in set_cookie.decode('utf-8').split(';'):
            key, value = attr.strip().split('=')
            cookies[key] = value
        return cookies

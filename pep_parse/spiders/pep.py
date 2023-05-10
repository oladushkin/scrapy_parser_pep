import re
import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        peps_tables = response.css('section[id=numerical-index]')
        for line in peps_tables.css('tr'):
            href = line.css('a::attr(href)')
            if href == []:
                continue
            yield response.follow(href[0], callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()
        x = re.search(r'(?P<version>PEP.\d{1,})...(?P<name>.*)', title)
        version, name = x.groups()
        data = {
            'number': version,
            'name': name,
            'status': response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get(),
        }
        yield PepParseItem(data)

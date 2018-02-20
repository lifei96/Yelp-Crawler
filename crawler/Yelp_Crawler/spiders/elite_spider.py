# -*- coding: utf-8 -*-

import scrapy
import re


class EliteSpider(scrapy.Spider):
    name = "elite"

    def start_requests(self):
        with open('data/urls.txt', 'r') as f:
            urls = f.read().split('\n')
        count = 0
        for url in urls:
            self.log('Requesting %s' % url)
            yield scrapy.Request(url=url, callback=self.parse)
            self.log('Finished %s' % url)
            count += 1
            self.log('%d/%d' % (count, len(urls)))

    def parse(self, response):
        username = re.findall('<h1>(.*?)</h1>', response.body)[0]
        elite_year_dict = {'url': response.url, 'name': username}
        for year in ['18', '17', '16', '15', '14', '13', '12', '11', '10', '09', '08', '07']:
            if len(re.findall('>’' + year + '</span>', response.body)) or \
                    len(re.findall('>Elite 20' + year + '</span>', response.body)):
                elite_year_dict[year] = 1
            else:
                elite_year_dict[year] = 0

        if elite_year_dict['17'] and (not elite_year_dict['16']):
            print 'Found!'
            with open('data/elite_17.txt', 'a') as f:
                f.write(response.url + '\n')

        yield elite_year_dict

# -*- coding: utf-8 -*-

from yelp_crawler import YelpCrawler

URLS_PATH = 'data/urls.txt'
ELITE_CSV_PATH = 'data/user_elite_years.csv'

if __name__ == '__main__':
    with open(URLS_PATH, 'r') as f:
        urls = f.read().split('\n')
    yelp_crawler = YelpCrawler()
    yelp_crawler.crawl_elite_years(urls, ELITE_CSV_PATH)

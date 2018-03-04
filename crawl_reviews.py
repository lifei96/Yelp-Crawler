# -*- coding: utf-8 -*-

from yelp_crawler import YelpCrawler
import pandas as pd

URLS_PATH = 'data/elite_17.csv'
REVIEW_CSV_PATH = 'data/reviews_elite_17.csv'

if __name__ == '__main__':
    df = pd.read_csv(URLS_PATH, encoding='utf-8')
    urls = df['url'].tolist()
    yelp_crawler = YelpCrawler()
    yelp_crawler.crawl_reviews(urls, REVIEW_CSV_PATH)

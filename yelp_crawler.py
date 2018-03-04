# -*- coding: utf-8 -*-

import re
import time

import pandas as pd
from util import *

TIME_INTERVAL = 5


class YelpCrawler(object):
    def __init__(self):
        pass

    def crawl_elite_years(self, urls, elite_csv_path):
        set_locale()
        driver = get_chrome_driver()
        users = []
        count = 0
        for url in urls:
            count += 1
            try:
                print '-----getting %s-----' % url
                driver.get(url)
                time.sleep(TIME_INTERVAL)
            except Exception as inst:
                print type(inst)
                print inst.args
                print inst
            page_source = driver.page_source.encode('utf-8')
            try:
                username = re.findall('<h1>(.*?)</h1>', page_source)[0]
            except:
                print '-----username not found-----'
                username = ''
            elite_year_dict = {'url': url, 'name': username}
            for year in ['18', '17', '16', '15', '14', '13', '12', '11', '10', '09', '08', '07']:
                if len(re.findall('>’' + year + '</span>', page_source)) or \
                        len(re.findall('>Elite 20' + year + '</span>', page_source)):
                    elite_year_dict[year] = 1
                else:
                    elite_year_dict[year] = 0
            users.append(elite_year_dict)
            print elite_year_dict
            print '-----Finished %d/%d-----' % (count, len(urls))
        driver.quit()
        df = pd.DataFrame(users)
        df.to_csv(elite_csv_path, index=False, encoding='utf-8')
        df = df[['name', 'url', '18', '17', '16', '15', '14', '13', '12', '11', '10', '09', '08', '07']]
        df.to_csv(elite_csv_path, index=False, encoding='utf-8')

    def crawl_reviews(self, urls, review_csv_path):
        set_locale()
        driver = get_chrome_driver()
        reviews = []
        count = 0
        for url in urls:
            count += 1
            try:
                print '-----getting %s-----' % url
                driver.get(url)
                time.sleep(TIME_INTERVAL)
            except Exception as inst:
                print type(inst)
                print inst.args
                print inst
            page_source = driver.page_source.encode('utf-8')

            try:
                username = re.findall('<h1>(.*?)</h1>', page_source)[0]
            except:
                print '-----username not found-----'
                username = ''

            try:
                location = re.findall('user-location alternate">(.*?)</h3>', page_source)[0]
            except:
                print '-----location not found-----'
                location = ''

            try:
                friend_count = int(driver.find_element_by_xpath("//*[@class='friend-count']/strong[1]").text)
            except:
                print '-----friend_count not found-----'
                friend_count = 0

            try:
                review_count = int(driver.find_element_by_xpath("//*[@class='review-count']/strong[1]").text)
            except:
                print '-----review_count not found-----'
                review_count = 0

            try:
                photo_count = int(driver.find_element_by_xpath("//*[@class='photo-count']/strong[1]").text)
            except:
                print '-----photo_count not found-----'
                photo_count = 0

            page_count = review_count / 10
            if review_count % 10:
                page_count += 1
            review_page_url_pattern = url.replace('user_details', 'user_details_reviews_self') + '&rec_pagestart='

            for i in range(page_count):
                review_page_url = review_page_url_pattern + str(i * 10)
                try:
                    print '-----getting %s-----' % review_page_url
                    driver.get(review_page_url)
                    time.sleep(TIME_INTERVAL)
                except Exception as inst:
                    print type(inst)
                    print inst.args
                    print inst
                all_reviews = driver.find_elements_by_xpath("//*[@class='review']")
                for review in all_reviews:
                    review_dict = {'url': url, 'name': username, 'user_location': location,
                                   'friend_count': friend_count,
                                   'review_count': review_count, 'photo_count': photo_count}

                    try:
                        restaurant_name = review.find_element_by_xpath(
                            ".//*[@class='biz-name js-analytics-click']/span[1]").text
                    except:
                        print '-----restaurant_name not found-----'
                        restaurant_name = ''
                    review_dict['restaurant_name'] = restaurant_name

                    try:
                        price_level = int(
                            review.find_element_by_xpath(".//*[@class='business-attribute price-range']").text.count(
                                '$'))
                    except:
                        # print '-----price_level not found-----'
                        price_level = 0
                    review_dict['price_level'] = price_level

                    try:
                        category_elements = review.find_elements_by_xpath(".//*[@class='category-str-list']/a")
                        category_list = []
                        for category_element in category_elements:
                            category_list.append(category_element.text)
                        categories = ','.join(category_list)
                    except:
                        # print '-----categories not found-----'
                        categories = ''
                    review_dict['categories'] = categories

                    try:
                        address_string = review.find_element_by_xpath(".//address[1]").get_attribute('innerHTML').strip()
                        address = address_string.split('<br>')[0]
                        city = address_string.split('<br>')[1]
                    except:
                        print '-----address not found-----'
                        address = ''
                        city = ''
                    review_dict['address'] = address
                    review_dict['city'] = city

                    try:
                        rating_string = review.find_element_by_xpath(
                            ".//*[@class='biz-rating biz-rating-large clearfix']").get_attribute('innerHTML')
                        rating = int(
                            re.findall('i-stars i-stars--regular-(.*?) rating-large" title=', rating_string)[0])
                    except:
                        print '-----rating not found-----'
                        rating = 0
                    review_dict['rating'] = rating

                    try:
                        date = review.find_element_by_xpath(".//*[@class='rating-qualifier']").text.strip()
                        date_month = date.split('/')[0]
                        date_day = date.split('/')[1]
                        date_year = date.split('/')[2]
                    except:
                        print '-----date not found-----'
                        date = ''
                        date_month = ''
                        date_day = ''
                        date_year = ''
                    review_dict['date'] = date
                    review_dict['date_month'] = date_month
                    review_dict['date_day'] = date_day
                    review_dict['date_year'] = date_year

                    try:
                        review.find_element_by_xpath(".//*[@class='Updated review']")
                        updated_review = 1
                    except:
                        # print '-----updated_review not found-----'
                        updated_review = 0
                    review_dict['updated_review'] = updated_review

                    try:
                        review_content = review.find_element_by_xpath(".//p[1]").text
                    except:
                        print '-----review_content not found-----'
                        review_content = ''
                    review_dict['review_content'] = review_content

                    try:
                        useful_count = review.find_element_by_xpath(
                            ".//*[@class='ybtn ybtn--small useful js-analytics-click']/span[@class='count']").text
                        if useful_count == '':
                            useful_count = 0
                        else:
                            useful_count = int(useful_count)
                    except:
                        print '-----useful_count not found-----'
                        useful_count = 0
                    review_dict['useful_count'] = useful_count

                    try:
                        funny_count = review.find_element_by_xpath(
                            ".//*[@class='ybtn ybtn--small funny js-analytics-click']/span[@class='count']").text
                        if funny_count == '':
                            funny_count = 0
                        else:
                            funny_count = int(funny_count)
                    except:
                        print '-----funny_count not found-----'
                        funny_count = 0
                    review_dict['funny_count'] = funny_count

                    try:
                        cool_count = review.find_element_by_xpath(
                            ".//*[@class='ybtn ybtn--small cool js-analytics-click']/span[@class='count']").text
                        if cool_count == '':
                            cool_count = 0
                        else:
                            cool_count = int(cool_count)
                    except:
                        print '-----cool_count not found-----'
                        cool_count = 0
                    review_dict['cool_count'] = cool_count

                    reviews.append(review_dict)

                    print review_dict

                print 'user: %d/%d' % (count, len(urls))
                print 'username: %s' % username
                print 'page: %d/%d' % (i + 1, page_count)

            df = pd.DataFrame(reviews)
            df.to_csv(review_csv_path, index=False, encoding='utf-8')
            df = df[['name', 'url', 'user_location', 'friend_count', 'review_count', 'photo_count', 'restaurant_name',
                     'price_level', 'categories', 'address', 'city', 'rating', 'date', 'date_month', 'date_day',
                     'date_year', 'updated_review', 'review_content', 'useful_count', 'funny_count', 'cool_count']]
            df.to_csv(review_csv_path, index=False, encoding='utf-8')

        df = pd.DataFrame(reviews)
        df.to_csv(review_csv_path, index=False, encoding='utf-8')
        df = df[['name', 'url', 'user_location', 'friend_count', 'review_count', 'photo_count', 'restaurant_name',
                 'price_level', 'categories', 'address', 'city', 'rating', 'date', 'date_month', 'date_day',
                 'date_year', 'updated_review', 'review_content', 'useful_count', 'funny_count', 'cool_count']]
        df.to_csv(review_csv_path, index=False, encoding='utf-8')

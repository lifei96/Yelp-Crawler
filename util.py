# -*- coding: utf-8 -*-

import locale
import time

from selenium import webdriver

TIME_INTERVAL = 5


def get_chrome_driver():
    print '-----starting Chrome driver-----'
    return webdriver.Chrome('./chromedriver')


def set_locale():
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')


def get_url(driver, url):
    try:
        print '-----getting %s-----' % url
        driver.get(url)
        time.sleep(TIME_INTERVAL)
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SummonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    securityKey = scrapy.Field()
    securityID = scrapy.Field()
    marketID = scrapy.Field() # 1：上海， 2：深圳
    name = scrapy.Field()

class KDayItem(scrapy.Item):
    securityKey = scrapy.Field()
    date = scrapy.Field()
    kid = scrapy.Field()
    preClose = scrapy.Field()
    open = scrapy.Field()
    close = scrapy.Field()
    low = scrapy.Field()
    high = scrapy.Field()
    volume = scrapy.Field()
    turnover = scrapy.Field()
    marketTime = scrapy.Field()
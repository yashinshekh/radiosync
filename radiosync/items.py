# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RadiosyncItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    directory = scrapy.Field()
    radio_name = scrapy.Field()
    address = scrapy.Field()
    country = scrapy.Field()
    genres = scrapy.Field()
    language = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    stream_link = scrapy.Field()


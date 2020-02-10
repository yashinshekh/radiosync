# -*- coding: utf-8 -*-
import scrapy
import csv
import os

class RadioSpider(scrapy.Spider):
    name = 'radio'
    allowed_domains = ['radio.net']
    start_urls = ['http://radio.net/']

    def parse(self, response):
        genres = response.xpath('.//a/@href[contains(.,"/genre/")]').extract()
        for genre in genres:
            yield scrapy.Request(response.urljoin(genre),callback=self.getstations)

    def getstations(self,response):
        links = response.xpath('.//*[@class="stationinfo-link"]/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getdata)

        nextlink = response.xpath('.//*[@class="pagination-direction-link pagination-direction-link-next"]/a/@href').extract_first()
        if nextlink:
            yield scrapy.Request(response.urljoin(nextlink),callback=self.getstations)

    def getdata(self,response):
        name = response.xpath('.//h1/text()').extract_first()

        if "radio.csv" not in os.listdir(os.getcwd()):
            with open("appradiofm.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow(['name'])

        with open("radio.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow([name])
            print([name])


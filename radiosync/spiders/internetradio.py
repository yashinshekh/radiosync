# -*- coding: utf-8 -*-
import scrapy
import os
import csv

class InternetradioSpider(scrapy.Spider):
    name = 'internetradio'
    allowed_domains = ['internet-radio.com']
    start_urls = ['https://www.internet-radio.com/']

    def parse(self, response):
        links = response.xpath('.//*[@class="panel-body text-capitalize text-center"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getdatas)

    def getdatas(self,response):
        links = response.xpath('.//*[@class="text-danger"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getdata)

        nextlink = response.xpath('.//*[@class="next"]/a/@href').extract_first()
        if nextlink:
            yield scrapy.Request(response.urljoin(nextlink),callback=self.getdatas)

    def getdata(self,response):
        title = response.xpath('.//h1/text()').extract_first()
        website = response.xpath('.//a[contains(.,"http")]/text()').extract_first()
        genre = response.xpath('.//a/@onclick[contains(.,"genreclick")]/../text()').extract_first()

        if 'internetradio.csv' not in os.listdir(os.getcwd()):
            with open("internetradio.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow(['title','website','genre'])

        with open("internetradio.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow([title,website,genre])
            print([title,website,genre])

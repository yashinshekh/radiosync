# -*- coding: utf-8 -*-
import scrapy
import csv
import os


class RadioguideSpider(scrapy.Spider):
    name = 'radioguide'
    allowed_domains = ['radioguide.fm']
    start_urls = ['https://www.radioguide.fm/countries']

    def parse(self, response):
        datas = response.xpath('.//*[@class="col-md-4 col-xs-6 col-sm-6"]/a').extract()
        for data in datas:
            sel = scrapy.Selector(text=data)
            link = sel.xpath('.//a/@href').extract_first()
            country = sel.xpath('.//a/p/text()').extract_first()
            print(country)
            yield scrapy.Request(response.urljoin(link),callback=self.getstations,meta={
                'country':country
            })

    def getstations(self,response):
        links = response.xpath('.//*[@class="clearfix countries"]/li/div/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getdata,meta={
                'country':response.meta.get('country')
            })

    def getdata(self,response):
        title = response.xpath('.//*[@itemprop="name"]/text()').extract_first()
        description = response.xpath('.//*[@itemprop="description"]/text()').extract_first()

        if "radioguide.csv" not in os.listdir(os.getcwd()):
            with open("radioguide.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow(['country','title','description'])

        with open("radioguide.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow([response.meta.get('country'),title,description])
            print([response.meta.get('country'),title,description])

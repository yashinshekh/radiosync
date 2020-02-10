# -*- coding: utf-8 -*-
import scrapy
import os
import csv


class MyradiosSpider(scrapy.Spider):
    name = 'myradios'
    allowed_domains = ['my-radios.com']
    start_urls = ['http://my-radios.com/']

    def parse(self, response):
        datas = response.xpath('.//*[@class="list-inline intro-social-buttons"]/li').extract()
        for data in datas:
            sel = scrapy.Selector(text=data)
            link = sel.xpath('.//a/@href').extract_first()
            country = sel.xpath('.//a/span/text()').extract_first()

            yield scrapy.Request(response.urljoin(link),callback=self.getstations,meta={
                'country':country
            })

    def getstations(self,response):
        links = response.xpath('.//*[@class="col-sm-3"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getdata,meta={
                'country':response.meta.get('country')
            })

    def getdata(self,response):
        title = response.xpath('.//*[@class="col-sm-4"]/h1/text()').extract_first()

        if 'myradios.csv' not in os.listdir(os.getcwd()):
            with open("myradios.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow([response.meta.get('country'),title])

        with open("myradios.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow([response.meta.get('country'),title])
            print([response.meta.get('country'),title])

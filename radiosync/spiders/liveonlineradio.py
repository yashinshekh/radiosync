# -*- coding: utf-8 -*-
import scrapy
import csv
import os

class LiveonlineradioSpider(scrapy.Spider):
    name = 'liveonlineradio'
    allowed_domains = ['liveonlineradio.net']
    start_urls = ['https://www.liveonlineradio.net/countries']

    def parse(self, response):
        datas = response.xpath('.//*[@class="countries__countries-list"]/li').extract()
        for data in datas:
            sel = scrapy.Selector(text=data)
            link = sel.xpath('.//a/@href').extract_first()
            country = sel.xpath('.//a/text()').extract_first()

            yield scrapy.Request(response.urljoin(link),callback=self.getstations,meta={
                'country':country
            })

    def getstations(self,response):
        links = response.xpath('.//*[@class="col-sm-4 col-md-4"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getdata,meta={
                'country':response.meta.get('country')
            })

        nextlink = response.xpath('.//a[contains(.,"→")]/@href').extract_first()
        if nextlink:
            yield scrapy.Request(response.urljoin(nextlink),callback=self.getstations,meta={
                'country':response.meta.get('country')
            })

    def getdata(self,response):
        title = response.xpath('.//h1/text()').extract_first()
        description = response.xpath('.//*[@class="entry-content"]/p[1]/text()').extract_first()
        website = response.xpath('.//a/strong/text()').extract_first()

        if "liveonlineradio" not in os.listdir(os.getcwd()):
            with open("liveonlineradio.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow(['country','title','description','website'])


        with open("liveonlineradio.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow([response.meta.get('country'),title,description,website])
            print([response.meta.get('country'),title,description,website])


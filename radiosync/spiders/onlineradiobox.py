# -*- coding: utf-8 -*-
import scrapy
import os
import csv


class OnlineradioboxSpider(scrapy.Spider):
    name = 'onlineradiobox'
    allowed_domains = ['onlineradiobox.com']
    start_urls = ['https://onlineradiobox.com/']

    def parse(self, response):
        links = response.xpath('.//*[@class="catalog__mainland-list"]/li/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getcountry)

    def getcountry(self,response):
        datas = response.xpath('.//*[@class="countries__countries-list tab-pane fade in active"]/li').extract()
        for data in datas:
            sel = scrapy.Selector(text=data)
            link = sel.xpath('.//a/@href').extract_first()
            country = sel.xpath('.//a/text()').extract_first()

            yield scrapy.Request(response.urljoin(link),callback=self.getstates,meta={
                'country':country
            })

    def getstates(self,response):
        links = response.xpath('.//*[@class="regions-list"]/li/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getstations,meta={
                'country':response.meta.get('country')
            })

    def getstations(self,response):
        stations = response.xpath('.//*[@class="stations__station__title"]/a/@href').extract()
        for station in stations:
            yield scrapy.Request(response.urljoin(station),callback=self.getdatas,meta={
                'country':response.meta.get('country')
            })

    def getdatas(self,response):
        title = response.xpath('.//*[@class="station__title"]/text()').extract_first()
        location = response.xpath('.//*[@itemprop="additionalProperty"]/text()').extract_first()
        try:
            tags = ', '.join(response.xpath('.//*[@class="station__tags"]/li/a/text()').extract())
        except:
            tags = ''
        description = response.xpath('.//*[@itemprop="description"]/text()').extract_first()
        website = response.xpath('.//*[@itemprop="url"]/@href').extract_first()
        facebook = response.xpath('.//*[@title="Facebook"]/@href').extract_first()
        twitter = response.xpath('.//*[@title="Twitter"]/@href').extract_first()
        wikipedia = response.xpath('.//*[@title="Wikipedia"]/@href').extract_first()

        if 'onlineradiobox.csv' not in os.listdir(os.getcwd()):
            with open("onlineradiobox.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow(['country','title','location','tags','description','website','facebook','twitter','wikipedia'])


        with open("onlineradiobox.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow([response.meta.get('country'),title,location,tags,description,website,facebook,twitter,wikipedia])
            print([response.meta.get('country'),title,location,tags,description,website,facebook,twitter,wikipedia])


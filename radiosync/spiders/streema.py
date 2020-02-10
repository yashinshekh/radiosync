# -*- coding: utf-8 -*-
import scrapy
import csv
import os

class StreemaSpider(scrapy.Spider):
    name = 'streema'
    allowed_domains = ['streema.com']
    start_urls = ['https://streema.com/radios']

    def parse(self, response):
        links = response.xpath('.//h4[contains(.,"Browse by region")]/following-sibling::ul/li/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getcountries)

    def getcountries(self,response):
        datas = response.xpath('.//*[@class="column col-md-3 col-sm-6"]/li').extract()
        for data in datas:
            sel = scrapy.Selector(text=data)
            link = sel.xpath('.//a/@href').extract_first()
            country = sel.xpath('.//a/text()').extract_first()
            yield scrapy.Request(response.urljoin(link),callback=self.getstates,meta={
                'country':country.strip()
            })

    def getstates(self,response):
        links = response.xpath('.//*[@class="geo-list"]/div/ul/li/a/@href[contains(.,"/radios/")]').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getcities,meta={
                'country':response.meta.get('country')
            })

    def getcities(self,response):
        links = response.xpath('.//*[@class="geo-list"]/div/ul/li/a/@href[contains(.,"/radios/")]').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getradios,meta={
                'country':response.meta.get('country')
            })

    def getradios(self,response):
        links = response.xpath('.//*[@class="item-name"]/h5/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getdata,meta={
                'country':response.meta.get('country')
            })

    def getdata(self,response):
        title = response.xpath('.//*[@itemprop="name"]/text()').extract_first()
        try:
            description = ' '.join(response.xpath('.//*[@class="truncated-text"]//text()').extract())
        except:
            description = ''
        website = response.xpath('.//*[@class="radio-website-link"]/@href').extract_first()
        facebook = response.xpath('.//a/@href[contains(.,"facebook.com")]').extract_first()
        twitter = response.xpath('.//a/@href[contains(.,"twitter.com")]').extract_first()
        wikipedia = response.xpath('.//a/@href[contains(.,"wikipedia.com")]').extract_first()
        phone = response.xpath('.//span[contains(.,"Phone:")]/text()').extract_first()

        if 'streema.csv' not in os.listdir(os.getcwd()):
            with open("streema.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow(['country','title','description','website','facebook','twitter','wikipedia','phone'])

        with open("streema.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow([response.meta.get('country'),title,description,website,facebook,twitter,wikipedia,phone])
            print([response.meta.get('country'),title,description,website,facebook,twitter,wikipedia,phone])


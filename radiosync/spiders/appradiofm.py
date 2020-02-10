# -*- coding: utf-8 -*-
import csv

import scrapy
import os

class AppradiofmSpider(scrapy.Spider):
    name = 'appradiofm'
    allowed_domains = ['appradiofm.com']
    start_urls = ['http://appradiofm.com/by-country/']

    def parse(self, response):
        datas = response.xpath('.//*[@class="col s12 m6 l4 margin-all"]/a').extract()
        for data in datas:
            sel = scrapy.Selector(text=data)
            link = sel.xpath('.//a/@href').extract_first()
            country = sel.xpath('.//*[@class="title titlebylist"]/text()').extract_first()

            yield scrapy.Request(response.urljoin(link),callback=self.getcountry,meta={
                'country':country
            })
        nextlink = response.xpath('.//a[contains(.,"Next")]/@href').extract_first()
        if nextlink:
            yield scrapy.Request(nextlink.replace('\\\\','//'),callback=self.parse)

    def getcountry(self,response):
        links = response.xpath('.//*[@class="col s12 m6 l4 margin-all"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(link,callback=self.getdata,meta={
                'country':response.meta.get('country')
            })

        nextlink = response.xpath('.//a[contains(.,"Next")]/@href').extract_first()
        if nextlink:
            yield scrapy.Request(nextlink.replace('\\\\','//'),callback=self.getcountry,meta={
                'country':response.meta.get('country')
            })

    def getdata(self,response):
        title = response.xpath('.//h3[@class="player-heading-new"]/text()').extract_first()
        genres = response.xpath('.//th[contains(.,"Genres")]/following-sibling::td/text()').extract_first()
        language = response.xpath('.//th[contains(.,"Language")]/following-sibling::td/text()').extract_first()
        location = response.xpath('.//th[contains(.,"Location")]/following-sibling::td/text()').extract_first()
        website = response.xpath('.//th[contains(.,"Website")]/following-sibling::td/a/text()').extract_first()
        callsign = response.xpath('.//th[contains(.,"CallSign")]/following-sibling::td/text()').extract_first()
        frequency = response.xpath('.//th[contains(.,"Frequency")]/following-sibling::td/text()').extract_first()
        type = response.xpath('.//th[contains(.,"Type")]/following-sibling::td/text()').extract_first()

        if "appradiofm.csv" not in os.listdir(os.getcwd()):
            with open("appradiofm.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow(['country','title','genres','language','location','website','callsign','frequency','type'])

        with open("appradiofm.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow([response.meta.get('country'),title,genres,language,location,website,callsign,frequency,type])
            print([response.meta.get('country'),title,genres,language,location,website,callsign,frequency,type])
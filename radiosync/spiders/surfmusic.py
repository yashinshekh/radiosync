# -*- coding: utf-8 -*-
import scrapy
import os
import csv

class SurfmusicSpider(scrapy.Spider):
    name = 'surfmusic'
    allowed_domains = ['surfmusic.de']
    start_urls = [
        'http://www.surfmusic.de/euro.htm',
        'http://www.surfmusic.de/afrika.htm',
        'http://www.surfmusic.de/amerika.htm',
        'http://www.surfmusic.de/asien.htm',
        'http://www.surfmusic.de/ozean.htm',
        'http://www.surfmusic.de/bundesland.htm'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        datas = response.xpath('.//*[@class="home"]/a').extract()
        for data in datas:
            sel = scrapy.Selector(text=data)
            link = sel.xpath('.//a/@href').extract_first()
            country = sel.xpath('.//a/text()').extract_first()
            yield scrapy.Request(response.urljoin(link),callback=self.getstations,meta={
                'country':country.strip()
            })

    def getstations(self,response):
        datas = response.xpath('.//tr').extract()
        for data in datas:
            sel = scrapy.Selector(text=data)
            name = sel.xpath('.//td[3]/a/text()').extract_first()
            link = sel.xpath('.//td[3]/a/@href').extract_first()
            format = sel.xpath('.//td[4]/text()').extract_first()
            city = sel.xpath('.//td[5]/text()').extract_first()

            if "appradiofm.csv" not in os.listdir(os.getcwd()):
                with open("appradiofm.csv","a") as f:
                    writer = csv.writer(f)
                    writer.writerow(['country','title','website','format','city'])

            if name:
                with open("appradiofm.csv","a") as f:
                    writer = csv.writer(f)
                    writer.writerow([response.meta.get('country'),name,link,format,city])
                    print([response.meta.get('country'),name,link,format,city])

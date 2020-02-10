# -*- coding: utf-8 -*-
import scrapy
import csv
import os
from ..items import RadiosyncItem
import json
import requests

class TuneinSpider(scrapy.Spider):
    name = 'tunein'
    allowed_domains = ['tunein.com']
    start_urls = ['https://tunein.com/radio/regions/']

    def parse(self, response):
        links = response.xpath('.//*[@class="guide-item__guideItemLink___3w_uL common__link___1BB3z"]/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getcountry)
            #break
            

    def getcountry(self,response):
        datas = response.xpath('.//*[@class="guide-item__guideItemLink___3w_uL common__link___1BB3z"]').extract()
        for data in datas:
            sel = scrapy.Selector(text=data)
            link = sel.xpath('.//*[@class="guide-item__guideItemLink___3w_uL common__link___1BB3z"]/@href').extract_first()
            country = sel.xpath('.//span/text()').extract_first()

            yield scrapy.Request(response.urljoin(link),callback=self.getstations,meta={
                'country':country
            })
            #break
            

    def getstations(self,response):
        links = response.xpath('.//*[@class="guide-item__guideItemLink___3w_uL common__link___1BB3z"]/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getstation,meta={
                'country':response.meta.get('country')
            })
            #break
            

    def getstation(self,response):
        links = response.xpath('.//*[@class="col-xs-12 guide-item__guideItemTitlesContainer___KyL02 common__verticalAlignChild___YF2vC guide-item__guideItemLink___3w_uL common__link___1BB3z"]/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getdata,meta={
                'country':response.meta.get('country')
            })
            

    def getdata(self,response):
        item = RadiosyncItem()
        item['country'] = response.meta.get('country')
        item['directory'] = self.allowed_domains[0]
        item['radio_name'] = response.xpath('.//h1/text()').extract_first()
        item['address'] = response.xpath('.//p[contains(.,"Location:")]/following-sibling::p/text()').extract_first()
        try:
            item['genres'] = ', '.join(response.xpath('.//p[contains(.,"Genres:")]/../a/p/text()').extract())
        except:
            item['genres'] = ''
        item['language'] = response.xpath('.//p[contains(.,"Language:")]/following-sibling::p/text()').extract_first()
        item['phone'] = response.xpath('.//p[contains(.,"Contact:")]/following-sibling::p/text()').extract_first()
        item['email'] = response.xpath('.//p[contains(.,"Email:")]/following-sibling::p/text()').extract_first()
        item['website'] = response.xpath('.//p[contains(.,"Website:")]/following-sibling::a/p/text()').extract_first()
        try:
            item['image_urls'] = ['https://cdn-radiotime-logos.tunein.com/'+str(response.url.split('-')[-1].replace('/',''))+'.png']
        except:
            item['image_urls'] = ''
        try:
            item['stream_link'] = json.loads(requests.get('https://opml.radiotime.com/Tune.ashx?id='+str(response.url.split('-')[-1].replace('/',''))+'&render=json&listenId=1581345268&formats=mp3,aac,ogg,flash,html,hls&type=station&us_privacy=1YNY&partnerId=RadioTime').text)['body'][0]['url']
        except:
            item['stream_link'] = ''

        yield item

    #     yield scrapy.Request('https://opml.radiotime.com/Tune.ashx?id='+str(response.url.split('-')[-1].replace('/',''))+'&render=json&formats=mp3,aac,ogg,flash,html,hls',callback=self.getstream,meta={
    #         'name':name,
    #         'location':location,
    #         'genre':genre,
    #         'language':language,
    #         'contact':contact,
    #         'website':website,
    #         'logo':logo,
    #         'country':response.meta.get('country')
    #     },dont_filter=True)
    #
    #
    # def getstream(self,response):
    #     item = RadiosyncItem()
    #     try:
    #         item['stream_link'] = json.loads(response.text)['body'][0]['url']
    #     except:
    #         item['stream_link'] = ''
    #     item['directory'] = self.allowed_domains[0]
    #     try:
    #         item['radio_name'] = response.meta.get('name')
    #     except:
    #         item['radio_name'] = ''
    #     try:
    #         item['address'] = response.meta.get('location')
    #     except:
    #         item['address'] = ''
    #     try:
    #         item['country'] = response.meta.get('country')
    #     except:
    #         item['country'] = ''
    #     try:
    #         item['genres'] = response.meta.get('genres')
    #     except:
    #         item['genres'] = ''
    #     try:
    #         item['language'] = response.meta.get('language')
    #     except:
    #         item['language'] = ''
    #     try:
    #         item['phone'] = response.meta.get('phone')
    #     except:
    #         item['phone'] = ''
    #     try:
    #         item['email'] = response.meta.get('email')
    #     except:
    #         item['email'] = ''
    #     try:
    #         item['image_urls'] = [response.meta.get('logo')]
    #     except:
    #         item['image_urls'] = ''
    #
    #     yield item




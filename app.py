from scrapy.crawler import CrawlerProcess

from radiosync.spiders.appradiofm import AppradiofmSpider
from radiosync.spiders.appradiofm import InternetradioSpider
from radiosync.spiders.appradiofm import LiveonlineradioSpider
from radiosync.spiders.appradiofm import MyradiosSpider
from radiosync.spiders.appradiofm import OnlineradioboxSpider
from radiosync.spiders.appradiofm import RadioSpider
from radiosync.spiders.appradiofm import RadioguideSpider
from radiosync.spiders.appradiofm import StreemaSpider
from radiosync.spiders.appradiofm import SurfmusicSpider
from radiosync.spiders.appradiofm import TuneinSpider

process = CrawlerProcess()
process.crawl(AppradiofmSpider)
process.crawl(InternetradioSpider)
process.crawl(LiveonlineradioSpider)
process.crawl(MyradiosSpider)
process.crawl(OnlineradioboxSpider)
process.crawl(RadioguideSpider)
process.crawl(RadioSpider)
process.crawl(StreemaSpider)
process.crawl(SurfmusicSpider)
process.crawl(TuneinSpider)

process.start()
__author__ = 'Satish'

import os
import json
import logging.config
import locale

import scrapy
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy import optional_features



class BaseLyricArchiveScraper(scrapy.Spider):
    optional_features.remove('boto')
    handle_httpstatus_list = [404]
    # interested_genres = ['Adult Alternative Pop/Rock','Adult Contemporary','Alternative Metal','Alternative Pop/Rock','British Metal']
    interested_genres = ['British Metal']
    pipeline=[]
    _logger = logging.getLogger(__name__)
    name = "Lyric_Archive_Base"
    alloweddomains = ["thelyricarchive.com/"]
    artist_page_urls = []
    album_page_urls = []
    baseurl = "http://www.thelyricarchive.com/"
    start_urls = [
        "http://www.thelyricarchive.com/genres/Rock/"
    ]

    def setup_logging(self,default_log_file_path='logging.json',default_level=logging.DEBUG,env_key = 'LOG_CFG'):
        """Setup logging configuration
        """
        path = default_log_file_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)


    def __init__(self, *args, **kwargs):
        self.setup_logging()
        self._logger = logging.getLogger(__name__)
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        self.failed_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def parse(self, response):
        self._logger.debug("Base Scraper - Res[pmse method for url %s ", response.url)
        hxs = Selector(response)
        #/html/body/table/tbody/tr[304]/td[2]/span[2]/a
        ##Get all the urls for the genre specific pages

        styles = hxs.xpath("//*[@class = 'stdmin']/tr/td/a/@href")
        for style in styles:
            print style.extract()
            if style.extract() in self.interested_genres:
                self._logger("Parsing the genre page for genre %s,with url ", style.extract())
                artists = hxs.xpath('/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr[3]/td[1]/a/@href')
                for artist in artists :
                    self._logger("Adding callback to parse page for Artist : %s ",artist.extract())
                    self.artist_page_urls.append(artist.extract())
                    yield scrapy.Request(artist.extract(),callback= self.parseArtistPage)



    def handle_spider_closed(self, spider, reason):  # added self
        self.crawler.stats.set_value('failed_urls', ','.join(spider.failed_urls))

    def process_exception(self, response, exception, spider):
        ex_class = "%s.%s" % (exception.__class__.__module__, exception.__class__.__name__)
        self._logger.error("Error url %s , Processing exception %s", response.url, ex_class)
        self.crawler.stats.inc_value('downloader/exception_count', spider=spider)
        self.crawler.stats.inc_value('downloader/exception_type_count/%s' % ex_class, spider=spider)

    def item_dropped(self, item, response, exception, spider):
        self._logger.error("Item dropped for url %s ", response.url)

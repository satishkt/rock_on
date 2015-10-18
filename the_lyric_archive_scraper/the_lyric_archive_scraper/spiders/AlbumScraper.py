from scrapy import Selector
from the_lyric_archive_scraper import pipelines
from the_lyric_archive_scraper.items import AlbumScraperItem
from the_lyric_archive_scraper.spiders.ArtistScraper import ArtistScraper
from the_lyric_archive_scraper.spiders.BaseScraper import BaseLyricArchiveScraper

__author__ = 'Satish'


class AlbumScraper(ArtistScraper):

    name = "albumScraper"

    def __init__(self):
        self.pipeline = [pipelines.JsonAlbum]
        ArtistScraper.__init__(self)

    def parseAlbumPage(self, response):

        self._logger.debug("Parsing Album Page at url %s ", response.url)
        artist_name = response.meta['artist_name']
        album_name = response.meta['album_name']
        self._logger.debug("Parsing Album %s for Artist %s", album_name, artist_name)
        hxs = Selector(response)
        album = AlbumScraperItem()
        album['album_name'] = album_name
        album['artist_name'] = artist_name

        album_label = hxs.xpath('/html/body/table[2]/tr/td[2]/table/tr[6]/td[2]/text()').extract()
        if (len(album_label) > 0):
            album['album_label'] = album_label[0]
        album_title = hxs.xpath('/html/body/table[2]/tr/td[2]/table/tr[2]/td[2]/text()').extract()
        if (len(album_title) > 0):
            print album_title[0]
        released_year = hxs.xpath('/html/body/table[2]/tr/td[2]/table/tr[3]/td[2]/text()').extract()
        if (len(released_year) > 0):
            album['album_year'] = released_year[0]
        album_styles = hxs.xpath('/html/body/table[2]/tr/td[2]/table/tr[5]/td[2]/ul/li')
        style_list = []
        for album_style in album_styles:
            style = album_style.xpath('./text()').extract()
            if (len(style) > 0):
                style_list.append(style[0])

        album['album_styles'] = ','.join(style_list)

        yield album

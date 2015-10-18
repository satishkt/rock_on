from scrapy import Selector
import scrapy
from the_lyric_archive_scraper import pipelines
from the_lyric_archive_scraper.items import ArtistScraperItem, AlbumScraperItem
from the_lyric_archive_scraper.spiders.BaseScraper import BaseLyricArchiveScraper

__author__ = 'Satish'


class ArtistScraper(BaseLyricArchiveScraper):
    name = "artistScraper"

    def __init__(self):
        self.pipeline = [pipelines.JsonArtist]
        BaseLyricArchiveScraper.__init__(self)

    def parseArtistPage(self, response):
        self._logger.debug("Parsing Artist Page at url %s ", response.url)
        hxs = Selector(response)
        artist = ArtistScraperItem()
        artist['item_type'] = 'Artist'

        artist_title = hxs.xpath('/html/body/table[1]/tr[1]/td/h1/text()').extract()[0]
        artist['artist_name'] = artist_title.rstrip('lyrics').strip()

        topsongs = hxs.xpath('/html/body/table[1]/tr[2]/td[3]/div/a/text()')
        if topsongs is not None:
            topsong_list = []
            for topsong in topsongs:
                topsong_list.append(topsong.extract().rstrip('lyrics').strip())
            artist['top_songs'] = ','.join(topsong_list)

        ##similar artists
        similar_artists = hxs.xpath('/html/body/table[1]/tr[3]/td/a/text()').extract()
        if (len(similar_artists) > 0):
            artist['similar_artists'] = similar_artists[0]

        grp_members = hxs.xpath('/html/body/table[1]/tr[2]/td[2]/table[2]/tr/td/a/text()')
        if (len(grp_members) > 0):
            grpmember_list = []
            for member in grp_members:
                grpmember_list.append(member.extract().strip())
            artist['group_members'] = ','.join(grpmember_list)
        artist_tbl = hxs.xpath('/html/body/table[1]/tr[2]/td[2]/table[1]')
        artist_tbl_trs = artist_tbl.xpath('tr')
        for tr in artist_tbl_trs:
            tds = tr.xpath('td')
            label_td = tds[0]
            val_td = tds[1]
            label = label_td.xpath('b/text()').extract()

            if len(label) > 0 and label[0] == 'Formed:':
                value = val_td.xpath('./text()').extract()
                artist['formed'] = value[0]
            if len(label) > 0 and label[0] == 'Disbanded:':
                value = val_td.xpath('./text()').extract()
                artist['disbanded'] = value[0]
            if len(label) > 0 and label[0] == 'Years active:':
                value = val_td.xpath('./text()').extract()
                artist['years_active'] = value[0]
            if len(label) > 0 and label[0] == 'Genre:':
                value = val_td.xpath('./text()').extract()
                artist['genre'] = value[0]
            if len(label) > 0 and label[0] == 'Styles:':
                style_val = []
                lis = val_td.xpath('ul/li')
                for li in lis:
                    li_val = li.xpath('./text()').extract()
                    if (len(li_val) > 0):
                        style_val.append(li_val[0])
                    artist['artist_styles'] = ','.join(style_val)
        yield artist

        album_links = hxs.xpath("//div[@style = 'float: left; padding:5px']/table//tr/td/strong/a")

        for album in album_links:
            request = scrapy.Request(album.xpath('@href').extract()[0], callback=self.parseAlbumPage)
            request.meta['artist_name'] = artist_title.rstrip('lyrics').strip()
            request.meta['album_name'] = album.xpath('text()').extract()[0]
            yield request

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

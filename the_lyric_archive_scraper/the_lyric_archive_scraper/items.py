# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

#
# Item class to hold Artist details
#
#

class ArtistScraperItem(scrapy.Item):
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key]= scrapy.Field()
        super(ArtistScraperItem, self).__setitem__(key, value)
    # define the fields for your item here like:
    # name = scrapy.Field()
    artist_name = scrapy.Field()
    formed = scrapy.Field()
    genre = scrapy.Field()
    years_active = scrapy.Field()
    artist_styles=scrapy.Field()
    similar_artists = scrapy.Field()
    top_songs=scrapy.Field()
    group_members = scrapy.Field()


#
# Item class to hold Album details
#
#


class AlbumScraperItem(scrapy.Item):
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key]= scrapy.Field()
        super(AlbumScraperItem, self).__setitem__(key, value)
    artist_name = scrapy.Field()
    album_name = scrapy.Field()
    album_year = scrapy.Field()
    album_styles =scrapy.Field()
    album_label = scrapy.Field()

#
# Item class to hold Lyrics for particular song
#
#

class SongLyricScraperItem(scrapy.Item):
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key]= scrapy.Field()
        super(SongLyricScraperItem, self).__setitem__(key, value)
    song_lyric = scrapy.Field()
    song_rating = scrapy.Field()
    song_composer = scrapy.Field()
    song_writer = scrapy.Field()
    artist_name = scrapy.Field()
    album_name = scrapy.Field()




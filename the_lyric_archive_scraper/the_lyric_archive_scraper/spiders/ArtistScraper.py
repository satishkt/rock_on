from the_lyric_archive_scraper import pipelines
from the_lyric_archive_scraper.spiders.BaseScraper import BaseLyricArchiveScraper

__author__ = 'Satish'

class ArtistScraper(BaseLyricArchiveScraper):

    name = "artistScraper"

    def __init__(self):
        self.pipeline=[pipelines.JsonArtist]
        BaseLyricArchiveScraper.__init__(self)

    def parseArtistPage(self,response):
        print "XXXX"



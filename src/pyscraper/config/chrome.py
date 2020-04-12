
from pyscraper.config import ScraperConfigBase


class ScraperConfigChrome(ScraperConfigBase):
    TYPE = 'chrome'
    def __init__(self):
        super().__init__()

    @property
    def type(self):
        return self.TYPE


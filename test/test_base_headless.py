

import unittest

from pyscraper import Scraper
from pyscraper import ScraperBaseHeadless
from pyscraper import ScraperConfigChrome

from selenium import webdriver


class ScraperBaseHeadlessTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cfg = ScraperConfigChrome()
        cfg.set('headless', True)

        exclude_switches = [
            'ignore-certificate-errors',
            'enable-automation',
            'enable-crash-reporter',
            'service-sandbox-type',
            'test-type',
            'enable-blink-features',
        ]
        cfg.add_exp_option('excludeSwitches', exclude_switches)
        cfg.add_exp_option('useAutomationExtension', False)
        cfg.add_service_args((
            ('verbose', None),
            ('log-path', './scraper.log'),
        ))

        scraper: ScraperBaseHeadless = Scraper.factory('base', cfg)

        cls.cfg = cfg
        cls.scraper = scraper

    def test_init(self):
        self.scraper.init()
        self.assertIsInstance(self.scraper.driver, webdriver.Chrome)

    def test_title(self):
        import re
        self.scraper.get('https://www.amazon.com')
        title = self.scraper.driver.title
        self.assertTrue(title.find('Amazon.com') >= 0)

        self.scraper.get('https://www.amazon.it')
        title = self.scraper.driver.title
        self.assertTrue(re.search('amazon.it', title, re.IGNORECASE))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(ScraperBaseHeadlessTestCase('test_init'))
    suite.addTest(ScraperBaseHeadlessTestCase('test_title'))
    return suite


runner = unittest.TextTestRunner(verbosity=3, failfast=True)
runner.run(suite())

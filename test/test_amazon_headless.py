

import unittest

from pyscraper import Scraper
from pyscraper import ScraperConfigChrome
from pyscraper import ScraperAmazonHeadless

from selenium import webdriver


class ScraperBaseTestCase(unittest.TestCase):

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

        scraper: ScraperAmazonHeadless = Scraper.factory('amazon', cfg)

        cls.cfg = cfg
        cls.scraper = scraper

    def test_init(self):
        self.scraper.init()
        self.assertIsInstance(self.scraper.driver, webdriver.Chrome)

    def test_title(self):
        import re
        self.scraper.get()
        title = self.scraper.driver.title
        self.assertTrue(re.search('amazon.com', title, re.IGNORECASE))

    def test_inject_jquery_ajax(self):
        self.skipTest('skip')

    def test_get_book_data1(self):
        scraper: ScraperAmazonHeadless = self.scraper

        scraper.select_search_category('Books')
        scraper.search('0321714113')
        scraper.wait_page_load()
        
        elem = scraper.get_first_product_elem()
        scraper.move_mouse_to_anchor_elem(elem)
        scraper.click_mouse(elem)
        scraper.wait_page_load()

        book = scraper.get_book_data()
        self.assertEqual(book.asin, '0321714113')

    def test_get_book_data2(self):
        scraper: ScraperAmazonHeadless = self.scraper

        scraper.select_search_category('Books')
        scraper.search('1788992512')
        scraper.wait_page_load()
        
        elem = scraper.get_first_product_elem()
        scraper.move_mouse_to_anchor_elem(elem)
        scraper.click_mouse(elem)
        scraper.wait_page_load()

        book = scraper.get_book_data()
        self.assertEqual(book.asin, '1788992512')
        


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ScraperBaseTestCase('test_init'))
    suite.addTest(ScraperBaseTestCase('test_title'))
    suite.addTest(ScraperBaseTestCase('test_get_book_data1'))
    suite.addTest(ScraperBaseTestCase('test_get_book_data2'))
    return suite


runner = unittest.TextTestRunner(verbosity=3, failfast=True)
runner.run(suite())

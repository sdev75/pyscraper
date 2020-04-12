

import unittest

from pyscraper import Scraper
from pyscraper import ScraperConfigChrome
from pyscraper import ScraperAmazon

from selenium import webdriver


class ScraperBaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cfg = ScraperConfigChrome()
        cfg.set('headless', False)

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

        scraper: ScraperAmazon = Scraper.factory('amazon', cfg)

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
        driver = self.scraper.driver
        val = driver.execute_script('return window._jai')
        self.assertTrue(val)

    def test_get_book_data1(self):
        scraper: ScraperAmazon = self.scraper

        self.scraper.get()
        scraper.select_search_category('Books')
        scraper.search('0321714113')
        scraper.wait_page_load()

        elem = scraper.get_first_product_elem()
        scraper.move_mouse_to_anchor_elem(elem)
        scraper.click_mouse()
        scraper.wait_page_load()

        book = scraper.get_book_data()
        self.assertEqual(book.asin, '0321714113')

    def test_get_book_data2(self):
        scraper: ScraperAmazon = self.scraper

        scraper.select_search_category('Books')
        scraper.search('1788992512')
        scraper.wait_page_load()
        
        elem = scraper.get_first_product_elem()
        scraper.move_mouse_to_anchor_elem(elem)
        scraper.click_mouse()
        scraper.wait_page_load()

        book = scraper.get_book_data()
        self.assertEqual(book.asin, '1788992512')

    def test_get_book_data_no_results(self):
        scraper: ScraperAmazon = self.scraper

        scraper.select_search_category('Books')
        scraper.search('745643563343')
        scraper.wait_page_load()
        
        elem = scraper.get_first_product_elem()
        self.assertFalse(elem)
        


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ScraperBaseTestCase('test_init'))
    suite.addTest(ScraperBaseTestCase('test_title'))
    suite.addTest(ScraperBaseTestCase('test_inject_jquery_ajax'))
    suite.addTest(ScraperBaseTestCase('test_get_book_data1'))
    suite.addTest(ScraperBaseTestCase('test_get_book_data2'))
    suite.addTest(ScraperBaseTestCase('test_get_book_data_no_results'))
    return suite


runner = unittest.TextTestRunner(verbosity=3, failfast=True)
runner.run(suite())

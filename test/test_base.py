

import unittest

from pyscraper import Scraper
from pyscraper import ScraperBase
from pyscraper import ScraperConfigChrome

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

        scraper: ScraperBase = Scraper.factory('base', cfg)

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

    def test_title_regex_match(self):
        scraper: ScraperBase = self.scraper
        scraper.get('https://www.amazon.de')
        title = scraper.driver.title
        self.assertTrue(scraper.wait_until_regex_match(
            r'^Amazon.de: Günstige Preise', title))

    def test_wait_page_load(self):
        scraper: ScraperBase = self.scraper
        scraper.get('http://example.com/')
        a = scraper.get_elem_by_xpath('/html/body/div/p[2]/a')
        scraper.move_mouse_to_anchor_elem(a)
        scraper.click_mouse()
        scraper.wait_until_new_page_load()

    def test_scroll(self):
        scraper: ScraperBase = self.scraper

        data = scraper.get_scroll_info()
        self.assertEqual(data['percent'], 0, 'Scroll position set to 0')

    def test_scroll_down(self):
        scraper: ScraperBase = self.scraper

        data = scraper.get_scroll_info()
        print(data)
        self.assertEqual(data['percent'], 0, 'Scroll position set to 0')

        data = scraper.scroll_to(data['height'])
        self.assertTrue(data['percent'] == 100, 'Scroll to bottom of screen')

    def test_scroll_up(self):
        scraper: ScraperBase = self.scraper

        data = scraper.scroll_to(0)
        self.assertEqual(data['percent'], 0, 'Scrolling back to top')

    def test_scroll_rand(self):
        import math
        import random
        scraper: ScraperBase = self.scraper

        data = scraper.get_scroll_info()
        n = random.randint(
            math.floor(0.25 * data['height']),
            math.floor(0.75 * data['height'])
        )
        data = scraper.scroll_to(n)
        self.assertGreaterEqual(data['top'], n, f'Scrolling to {n}')

        data = scraper.scroll_to(0)
        self.assertEqual(data['percent'], 0, 'Scrolling back to top')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ScraperBaseTestCase('test_init'))
    suite.addTest(ScraperBaseTestCase('test_title'))
    suite.addTest(ScraperBaseTestCase('test_title_regex_match'))
    suite.addTest(ScraperBaseTestCase('test_wait_page_load'))
    suite.addTest(ScraperBaseTestCase('test_scroll'))
    suite.addTest(ScraperBaseTestCase('test_scroll_down'))
    suite.addTest(ScraperBaseTestCase('test_scroll_up'))
    suite.addTest(ScraperBaseTestCase('test_scroll_rand'))
    return suite


runner = unittest.TextTestRunner(verbosity=3, failfast=True)
runner.run(suite())

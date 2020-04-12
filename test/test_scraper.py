

import unittest

from pyscraper import ScraperConfigBase, ScraperConfigChrome
from pyscraper import ScraperBase, ScraperBaseHeadless
from pyscraper import ScraperAmazon, ScraperAmazonHeadless
from pyscraper import Scraper


class ScraperTestCase(unittest.TestCase):

    def test_scraper(self):
        scraper = Scraper()
        self.assertIsInstance(scraper, Scraper)

    def test_config(self):
        with self.assertRaises(TypeError):
            ScraperConfigBase()

        cfg = ScraperConfigChrome()
        self.assertEqual(cfg.type, 'chrome')

    def test_base(self):
        cfg = ScraperConfigChrome()
        scraper: ScraperBase = Scraper.factory('base', cfg)
        self.assertIsInstance(scraper, ScraperBase)

    def test_base_headless(self):
        cfg = ScraperConfigChrome()
        cfg.set('headless', True)
        scraper: ScraperBaseHeadless = Scraper.factory('base', cfg)
        self.assertIsInstance(scraper, ScraperBaseHeadless)

    def test_amazon(self):
        cfg = ScraperConfigChrome()
        scraper: ScraperAmazon = Scraper.factory('amazon', cfg)
        self.assertIsInstance(scraper, ScraperAmazon)

    def test_amazon_headless(self):
        cfg = ScraperConfigChrome()
        cfg.set('headless', True)
        scraper: ScraperAmazonHeadless = Scraper.factory('amazon', cfg)
        self.assertIsInstance(scraper, ScraperAmazonHeadless)

    def test_base_with_options(self):
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
            ('log-path', './scraper_base.log'),
        ))

        scraper: ScraperBase = Scraper.factory('base', cfg)

        self.assertListEqual(
            scraper.cfg.exp_options['excludeSwitches'], exclude_switches)
        self.assertFalse(
            scraper.cfg.exp_options['useAutomationExtension'], False)
        self.assertFalse('useAutomationExtension2' in scraper.cfg.exp_options)
        self.assertTrue('--verbose' in scraper.cfg.service_args)
        self.assertTrue(
            '--log-path=./scraper_base.log' in scraper.cfg.service_args)
        self.assertFalse('log-path2' in scraper.cfg.service_args)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ScraperTestCase('test_scraper'))
    suite.addTest(ScraperTestCase('test_config'))
    suite.addTest(ScraperTestCase('test_base'))
    suite.addTest(ScraperTestCase('test_base_headless'))
    suite.addTest(ScraperTestCase('test_amazon'))
    suite.addTest(ScraperTestCase('test_amazon_headless'))
    suite.addTest(ScraperTestCase('test_base_with_options'))
    return suite


runner = unittest.TextTestRunner(verbosity=3, failfast=True)
runner.run(suite())

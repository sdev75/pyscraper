
from .config import ScraperConfigBase
from .base import ScraperBase, ScraperBaseHeadless
from .amazon import ScraperAmazon, ScraperAmazonHeadless


class Scraper:

    @staticmethod
    def factory(id, cfg: ScraperConfigBase, *args, **kwargs):
        headless = False
        if cfg.get('headless'):
            headless = True
            cfg.set('opendevtools', False)
            cfg.add_option('headless')
            cfg.add_option('no-sandbox')
            cfg.add_option('disable-gpu')

        cfg.add_option('disable-dev-shm-usage')
        cfg.add_option("incognito")
        cfg.add_option("profile-directory=Default")
        cfg.add_option("disable-plugins-discovery")
        cfg.add_option("disable-extensions")
        cfg.add_option("start-maximized")

        if cfg.get('opendevtools'):
            cfg.add_option("auto-open-devtools-for-tabs")

        if id == 'amazon':
            if headless:
                return ScraperAmazonHeadless(cfg, *args, **kwargs)
            return ScraperAmazon(cfg, *args, **kwargs)

        if id == 'base':
            if headless:
                return ScraperBaseHeadless(cfg, *args, **kwargs)
            return ScraperBase(cfg, *args, **kwargs)

        raise Exception('Invalid scraper ID requested')

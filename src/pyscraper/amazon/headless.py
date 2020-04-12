
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from pyscraper.base import ScraperBaseHeadless
from .base import ScraperAmazon
from .model.book import AmazonBook


class ScraperAmazonHeadless(ScraperBaseHeadless, ScraperAmazon):
    def __init__(self, cfg):
        super().__init__(cfg)

    def select_search_category(self, text):
        elem = self.get_search_dropdown_elem()
        select = Select(elem)
        self.move_mouse_to_elem(elem)
        self.click_mouse(elem)
        select.select_by_visible_text(text)

    def search(self, text):
        elem = self.get_search_input_elem()
        self.move_mouse_to_elem(elem)
        self.click_mouse(elem)
        self.send_keys_delayed(elem, text)

        chain = ActionChains(self.driver)
        chain.send_keys(Keys.ENTER)
        chain.perform()

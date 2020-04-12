
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
import random
import math
import sys

from .base import ScraperBase


class ScraperBaseHeadless(ScraperBase):
    def __init__(self, cfg):
        super().__init__(cfg)

    def scroll_to(self, y):
        self.driver.execute_script(f'window.scrollTo(0, {y})')

    def move_mouse_to_coords(self, x, y):
        ActionChains(self.driver).move_by_offset(x, y).perform()

    def move_mouse_to_elem(self, elem: WebElement):
        ActionChains(self.driver).move_to_element(elem).perform()

    def click_mouse(self, elem: WebElement):
        ActionChains(self.driver).click(elem).perform()

    def move_mouse_to_anchor_elem(self, elem: WebElement, text='', wait=True):
        self.move_mouse_to_elem(elem)

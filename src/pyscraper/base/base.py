from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

import random
import time
import pyautogui
import pyclick
import math
import json

from threading import Thread

from pyscraper import ScraperConfigBase
from pyscraper import ScraperUtils


class ScraperBase:

    options = Options()
    service_args = []
    _init = False
    _old_page_id = 0

    def __init__(self, cfg: ScraperConfigBase):
        for opt in cfg.options:
            self.options.add_argument(opt)

        for k, v in cfg.exp_options.items():
            self.options.add_experimental_option(k, v)

        self.service_args = cfg.service_args
        self.cfg = cfg

    def init(self):
        if self._init:
            return

        if self.cfg.type == 'chrome':
            self.driver = webdriver.Chrome(
                options=self.options, service_args=self.service_args)
            useragent = self.getDriverUseragent().replace('HeadlessChrome', 'Chrome')
            self.driver.execute_cdp_cmd('Emulation.setUserAgentOverride', {
                'userAgent': useragent})
        else:
            raise Exception('Driver type not yet supported!')

        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''Object.defineProperty(navigator, 'webdriver',{get:()=>undefined});'''
        })

        self.driver.execute_cdp_cmd('Network.enable', {})

        self._init = True

    def close(self):
        if self._init:
            self.driver.close()
            self._init = False

    def __del__(self):
        self.close()

    def get(self, url):
        self.driver.get(url)
        self._old_page_id = self.get_page_id()
        return self._old_page_id

    def getNavigatorUseragent(self):
        return self.driver.execute_script('return navigator.userAgent')

    def getDriverUseragent(self) -> str:
        res = self.driver.execute_cdp_cmd('Browser.getVersion', {})
        return res['userAgent']

    @property
    def humanclicker(self) -> pyclick.HumanClicker:
        if not hasattr(self, '_humanclicker'):
            self._humanclicker = pyclick.HumanClicker()
        return self._humanclicker

    def send_keys_delayed(self, elem: WebElement, text: str):
        for keys in ScraperUtils.text_to_rand_chunks(text):
            elem.send_keys(keys)
            time.sleep(random.uniform(0.1, 1.0))

    def get_document_webdriver(self):
        return self.driver.execute_script('return window.navigator.webdriver')

    def get_panel_height(self):
        return self.driver.execute_script('return window.outerHeight - window.innerHeight')

    def get_elem_abs_pos(self, elem: WebElement) -> dict:
        x = elem.location['x']
        y = elem.location['y'] + self.get_panel_height()
        return (x, y)

    def move_mouse_to_coords(self, x, y):
        pos = pyautogui.position()
        knotsCount = random.randint(2, 10)
        duration = random.uniform(0.25, 0.75)

        curve = pyclick.HumanCurve((pos[0], pos[1]), (x, y),
                                   knotsCount=knotsCount,
                                   distortionMean=2,
                                   distortionStdev=3,
                                   distortionFrequency=1,
                                   targetPoints=100)

        self.humanclicker.move(toPoint=curve.toPoint,
                               duration=duration, humanCurve=curve)

    def move_mouse_to_elem(self, elem: WebElement, offset_x=0, offset_y=0, wait=True):
        pos = self.get_elem_abs_pos(elem)

        if offset_x or offset_y:
            pos = (pos[0] + offset_x, pos[1] + offset_y)

        def callback_closure(scraper, pos):
            def callback(driver):
                scraper.move_mouse_to_coords(pos[0], pos[1])
                return True
            return callback

        cb = callback_closure(self, pos)

        if wait:
            WebDriverWait(self.driver, timeout=5).until(cb)
            return

        cb(pos)

    def move_mouse_to_anchor_elem(self, elem: WebElement, text='', wait=True):
        # ensure the entire anchor rect is clickable
        self.driver.execute_script(
            'arguments[0].style.display = "inline-block";', elem)
        rand_x = random.randint(math.floor(
            0.2*elem.size['width']), math.floor(0.9*elem.size['width']))
        rand_y = random.randint(math.floor(
            0.2*elem.size['height']), math.floor(0.9*elem.size['height']))
        self.move_mouse_to_elem(elem, rand_x, rand_y, wait)

    def click_mouse(self):
        self.humanclicker.click()

    def get_scroll_position(self):
        return self.driver.execute_script('return document.documentElement.scrollTop')

    def get_scroll_height(self):
        return self.driver.execute_script('return document.body.scrollHeight')

    def has_scroll_reached_bottom(self) -> bool:
        return self.driver.execute_script('return (window.innerHeight + window.scrollY) >= document.body.offsetHeight')

    def get_scroll_info(self) -> int:
        data = self.driver.execute_script('''
            var h = document.documentElement,
                b = document.body,
                st = 'scrollTop',
                sh = 'scrollHeight';
            var shv = (h[sh]||b[sh]);
            var stv = (h[st]||b[st]);
            res = {
                scrollable: shv > h.clientHeigh,
                height: shv,
                top: stv,
                percent: stv / (shv - h.clientHeight) * 100 || 0,
                bottomed: (window.innerHeight + \
                           window.scrollY) >= b.offsetHeight
            };
            return res;
        ''')
        return data

    def get_elem_by_xpath(self, xpath):
        try:
            elem = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        except Exception as e:
            raise e

        return elem

    def get_page_id(self):
        elem = self.driver.find_element_by_tag_name('html')
        return elem.id

    def scroll_to(self, y):

        def closure(scraper, y):
            def callback(driver):
                pos = scraper.get_scroll_position()
                if pos <= y:
                    while(True):
                        # scrolling down
                        n = scraper.get_scroll_position()
                        if scraper.has_scroll_reached_bottom():
                            break

                        if n >= y:
                            break

                        pyautogui.scroll(-2)

                    return True

                if pos >= y:
                    while(True):
                        # scrolling up
                        n = scraper.get_scroll_position()
                        if n > 0 or n > y:
                            pyautogui.scroll(2)
                            continue
                        break

                    return True

                return True
            return callback

        cb = closure(self, y)

        WebDriverWait(self.driver, timeout=10).until(cb)
        return self.get_scroll_info()

    def wait_until_title_contains(self, title, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.title_contains(title))

    def wait_until_regex_match(self, pattern, text, timeout=10):
        import re

        def closure():
            regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE)

            def callback(driver):
                if regex.search(text):
                    return True
                return False
            return callback

        cb = closure()
        return WebDriverWait(self.driver, timeout=10).until(cb)

    def wait_until_elem_exists(self, id, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.ID, id)))

    def wait_until_new_page_load(self, old_page_id=0, timeout=10):
        if old_page_id == 0:
            old_page_id = self._old_page_id

        def closure(old_id):
            def callback(driver):
                id = driver.find_element_by_tag_name('html').id
                if id != old_id:
                    return id
                return False
            return callback

        cb = closure(old_page_id)
        return WebDriverWait(self.driver, timeout=10).until(cb)

    def wait_until_page_loaded(self, timeout=10):
        def cb(driver):
            status = driver.execute_script('return document.readyState')
            if status == 'complete':
                return True
            return False

        WebDriverWait(self.driver, timeout=10).until(cb)

    def wait_page_load(self, timeout=10):
        self.wait_until_new_page_load(timeout=timeout)
        self.wait_until_page_loaded(timeout)

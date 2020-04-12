from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import random
import time
import json

from pyscraper.config import ScraperConfigBase
from pyscraper.base import ScraperBase
from .model.book import AmazonBook


class ScraperAmazon(ScraperBase):
    def __init__(self, cfg: ScraperConfigBase):
        super().__init__(cfg)

    def init(self):
        super().init()
        self.inject_jquery_ajax_interceptor()

    def get(self, url='https://www.amazon.com/'):
        self.inject_jquery_ajax_interceptor()
        self.driver.get(url)
        return self.get_page_id()

    def get_search_input_elem(self) -> WebElement:
        return self.driver.find_element_by_id('twotabsearchtextbox')

    def get_search_dropdown_elem(self) -> WebElement:
        return self.driver.find_element_by_id('searchDropdownBox')

    def select_search_category(self, text):
        elem = self.get_search_dropdown_elem()
        select = Select(elem)
        self.move_mouse_to_elem(elem, 5, 5)
        self.click_mouse()
        select.select_by_visible_text(text)

    def search(self, text):
        elem = self.get_search_input_elem()
        elem.clear()
        self.move_mouse_to_elem(elem, 12, 15)
        self.click_mouse()
        self.send_keys_delayed(elem, text)

        chain = ActionChains(self.driver)
        chain.send_keys(Keys.ENTER)
        chain.perform()

    def inject_jquery_ajax_interceptor(self):
        script = '''
        console.log('inject_jquery_ajax_interceptor()');

        inject_jquery_ajax_interceptor = false;
        _jai = true;

        function defer(method) {
            if (window.jQuery) {
                method();
                return;
            }

            setTimeout(function() { defer(method) }, 100);
        }
        defer(function(){
            if(inject_jquery_ajax_interceptor){
                return;
            }
            jQuery(document).ajaxComplete(function(event, xhr, settings) {
                if (settings.url === '/gp/search-inside/service-data'){
                    if (settings.data.includes('method=getBookData')){
                        let el = document.getElementById('scraper-getbookdata');
                        if(!el){
                            el = document.createElement('div');
                            el.id = 'scraper-getbookdata';
                            el.hidden = true;
                            document.body.appendChild(el);
                        }
                        el.setAttribute('data-json',xhr.responseText.trim());
                        console.log(el);
                        console.log("FOUND!",[event,xhr,settings]);
                    }
                }
            });
            inject_jquery_ajax_interceptor = true;
            console.log(
                'inject_jquery_ajax_interceptor() injected successfully');
        });
        '''
        self.driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument', {'source': script})

    def get_first_product_elem(self):
        return self.get_elem_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[4]/div[1]/div[1]/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a')

    def get_book_data(self, timeout=5) -> AmazonBook:
        id = 'scraper-getbookdata'
        try:
            elem = self.wait_until_elem_exists(id)
            data = elem.get_attribute('data-json')
            return AmazonBook(json.loads(data))

        except NoSuchElementException:
            return False
        except TimeoutException:
            return False
        except Exception as e:
            raise e

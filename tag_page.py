from datetime import datetime
from time import sleep
import re
import pickle
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver


TAG_PAGE_URL = "https://www.instagram.com/explore/tags/{}/"
POST_ELEMENTS_SELECTOR = ".eLAPa"
POPUP_ELEMENT_SELECTOR = "div[role='dialog']"
ACCOUNT_NAME_ELEMENT_SELECTOR = ".ZIAjV"


class TagPage:
    def __init__(self, tag, numposts, browser, logging):
        self.browser = browser
        self.tag = tag
        self.numposts = numposts
        self.logging = logging
        if self.get_tag_page():
            return self.process_posts()
        else:
            return False

    def get_tag_page(self):
        self.logging.info("fetching tag page")
        url = TAG_PAGE_URL.format(self.tag)
        self.logging.info(url)
        self.browser.get(url)
        return self.test_load_success()

    def test_load_success(self):
        # todo this is a placeholder test
        return True

    def force_continious_scroll(self, scroll_count=5):
        # try to force the continious scroll
        for scroll_counter in range(scroll_count):
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            # sleep for a bit
            sleep(3)

    def extract_post_data(self, post_element):
        # find all the tags in the popups text

        account_element = (
            WebDriverWait(self.browser, 20)
            .until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ACCOUNT_NAME_ELEMENT_SELECTOR)
                )
            )
            .text
        )

        tags = re.findall("\#\S*", post_element.text)
        like_data = re.search("Liked by\s*\S*\s*and\s*(\d*)", post_element.text)
        account_element = post_element.find_element_by_css_selector(
            ACCOUNT_NAME_ELEMENT_SELECTOR
        )

        if like_data:
            like_count = like_data.groups()[0]
        else:
            like_count = 0

        return (account_element.text, like_count, tags)

    # overly complicated looking function to select the next post
    # this is required becuase the list on the page is dynamic so
    # you cant just pre select them and iterate
    # so instead we remember the previous one then loop over them to
    # find the one after the previous elemnt
    def get_next_element(self):
        post_elements = self.browser.find_elements_by_css_selector(
            POST_ELEMENTS_SELECTOR
        )
        # return  the first one if there is no previous
        if self.previously_found_element is None:
            self.previously_found_element = post_elements[0]
        else:
            element_is_found = False
            for element in post_elements:
                if element_is_found:
                    self.previously_found_element = element
                    break
                if element == self.previously_found_element:
                    element_is_found = True
        # TODO: handle end of list cleanly or no elements found
        return self.previously_found_element

    def process_posts(self):
        self.previously_found_element = None
        prev_element = None
        element_counter = 0
        results = []

        for element_counter in range(self.numposts):
            element = self.get_next_element()
            self.logging.info("tag element {}".format(element_counter))
            # scroll the element into view
            # cant click on it if not in viewport
            # this also causes the continious scroll to trigger
            self.browser.execute_script("arguments[0].scrollIntoView();", element)
            # TODO: try removing this
            sleep(1)

            element.click()

            # wait for it to load
            # TODO better wait
            sleep(2)

            popup_element = self.browser.find_element_by_css_selector(
                POPUP_ELEMENT_SELECTOR
            )

            el_data = self.extract_post_data(popup_element)
            results.append(el_data)

            webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
            prev_element = element
            sleep(1)

            if element_counter % 10 == 0:
                self.save_results(results, True)

            self.save_results(results)

    def save_results(self, results, temp_file=False):
        datetime_str = datetime.now().strftime("%Y%m%d")
        temp = ".temp"
        if not temp_file:
            temp = ""
        filename = "data/{}{}{}.tagdata".format(self.tag, datetime_str, temp)
        with open(filename, "wb") as f:
            pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

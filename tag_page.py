from datetime import datetime
from time import sleep
import re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pickle


TAG_PAGE_URL = "https://www.instagram.com/explore/tags/{}/"
POST_ELEMENTS_SELECTOR = ".eLAPa"
POPUP_ELEMENT_SELECTOR = "div[role='dialog']"
ACCOUNT_NAME_ELEMENT_SELECTOR = ".ZIAjV"


class TagPage:
    def __init__(self, tag, browser, logging):
        self.browser = browser
        self.tag = tag
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

    def process_posts(self):
        element_counter = 0
        results = []

        # load up a few pages of results
        # self.force_continious_scroll(5)

        for element_counter in range(100):
            post_elements = self.browser.find_elements_by_css_selector(
                POST_ELEMENTS_SELECTOR
            )

            element = post_elements[element_counter]
            print(element)
            self.logging.info("tag element {}".format(element_counter))
            # scroll the element into view

            self.browser.execute_script("arguments[0].scrollIntoView();", element)
            # webdriver does not work
            # webdriver.ActionChains(self.browser).move_to_element(element).perform()
            sleep(1)
            # click on the post element on the page
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
            sleep(2)

            if element_counter % 10 == 0:
                print(results)
                datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
                self.save_results(results, datetime_str + self.tag + ".data")

    def save_results(self, results, filename):
        with open(filename, "wb") as f:
            pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

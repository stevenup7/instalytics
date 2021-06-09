from time import sleep
import re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

TAG_PAGE_URL = "https://www.instagram.com/explore/tags/{}/"
POST_ELEMENTS_SELECTOR = ".eLAPa"
POPUP_ELEMENT_SELECTOR = "div[role='dialog']"
ACCOUNT_NAME_ELEMENT_SELECTOR = ".ZIAjV"


class TagPage:
    def __init__(self, tag, browser, logging):
        self.browser = browser
        self.tag = tag
        self.logging = logging
        self.logging.info("tagpage init " + self.tag)
        if self.get_tag_page():
            return self.process_posts()
        else:
            return False

    def get_tag_page(self):
        self.logging.info("fetching tag page")
        url = TAG_PAGE_URL.format(self.tag)
        self.logging.info(url)
        self.browser.get(url)
        self.logging.info(url)
        return self.test_load_success()

    def test_load_success(self):
        self.logging.info("testing success")
        # todo this is a placeholder test forg
        return True

    def process_posts(self):
        self.browser
        element_counter = 0

        # try to force the continious scroll
        for scroll_counter in range(5):
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            # sleep for a bit
            sleep(3)

        post_elements = self.browser.find_elements_by_css_selector(
            POST_ELEMENTS_SELECTOR
        )

        for element in post_elements:
            element_counter += 1
            # click on the post element on the page
            element.click()
            # wait for it to load
            # TODO better wait

            sleep(2)
            popup_element = self.browser.find_element_by_css_selector(
                POPUP_ELEMENT_SELECTOR
            )
            # find all the tags in the popups text
            tags = re.findall("\#\S*", popup_element.text)
            like_data = re.search("Liked by\s*\S*\s*and\s*(\d*)", popup_element.text)
            account_element = popup_element.find_element_by_css_selector(
                ACCOUNT_NAME_ELEMENT_SELECTOR
            )

            print(account_element.text, like_data.groups()[0], tags)
            webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
            sleep(2)

            # just in case break after 100 elements
            if element_counter > 2:
                break

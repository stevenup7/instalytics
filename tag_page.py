from datetime import datetime
from pagewrapper import PageWrapper
from time import sleep
import re
import pickle
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


TAG_PAGE_URL = "https://www.instagram.com/explore/tags/{}/"
POST_ELEMENTS_SELECTOR = ".eLAPa"
POPUP_ELEMENT_SELECTOR = "div[role='dialog']"
ACCOUNT_NAME_ELEMENT_SELECTOR = ".ZIAjV"
MORE_OPTIONS_MENU_BUTTON_SELECTOR = "svg[aria-label='More options']"
MORE_OPTIONS_MENU = ".mt3GC"


class TagPage(PageWrapper):
    """Loads up the search results page for a give tag and cycles through
    all the elements extracting data from them finally saves out to a
    data file"""

    def __init__(self, tag, numposts, browser, logging):
        super().__init__(browser, logging)
        self.tag = tag
        self.numposts = numposts
        if self.get_tag_page():
            return self.process_posts()
        else:
            return False

    def fetch_tag_page(self):
        self.logging.info("fetching tag page")
        url = TAG_PAGE_URL.format(self.tag)
        self.logging.info(url)
        self.browser.get(url)
        return self.test_load_success()

    def test_load_success(self):
        # todo this is a placeholder test
        return True

    def open_more_options_menu_and_get_link(self):
        self.browser.find_elements_by_css_selector(MORE_OPTIONS_MENU_BUTTON_SELECTOR)[
            0
        ].click()
        # wait for menu element to pop up
        self.wait_for_class(MORE_OPTIONS_MENU)
        self.find_element_by_text("Copy Link").click()
        link = self.get_clipboard_contents()
        return link

    def extract_post_data(self, post_element):
        """Wait for the popup to load and extract the following data
        - account name
        - likes
        - tags
        - link (assuming this is a unique id)
        """
        postdata = dict()

        # wait for the popup to load by checking for the acccount name element
        account_element = self.wait_for_class(ACCOUNT_NAME_ELEMENT_SELECTOR)
        postdata["account_name"] = account_element.text
        postdata["link"] = self.open_more_options_menu_and_get_link()
        postdata["tags"] = re.findall("\#\S*", post_element.text)

        like_data = re.search("Liked by\s*\S*\s*and\s*(\d*)", post_element.text)
        if like_data:
            postdata["like_count"] = like_data.groups()[0]
        else:
            postdata["like_count"] = 0

        return postdata

    def get_next_element(self):
        """Overly complicated looking function to select the next post
        this is required becuase the list on the page is dynamic so
        you cant just pre select them and iterate
        so instead we remember the previous one then loop over them to
        find the one after the previous element"""

        post_elements = self.browser.find_elements_by_css_selector(
            POST_ELEMENTS_SELECTOR
        )

        # return  the first one if there is no previous
        if self.__previously_found_element is None:
            self.__previously_found_element = post_elements[0]
        else:
            element_is_found = False
            for element in post_elements:
                if element_is_found:
                    self.__previously_found_element = element
                    break
                if element == self.__previously_found_element:
                    element_is_found = True
        # TODO: handle end of list cleanly or no elements found
        return self.__previously_found_element

    def process_posts(self):
        self.__previously_found_element = None
        prev_element = None
        element_counter = 0
        results = []

        for element_counter in range(self.numposts):
            element = self.get_next_element()
            self.logging.info("tag element {}".format(element_counter))
            # scroll the element into view
            # cant click on it if not in viewport
            # this also causes the continious scroll to trigger
            self.scroll_element_into_view(element)
            element.click()
            popup_element = self.wait_for_class(POPUP_ELEMENT_SELECTOR)
            el_data = self.extract_post_data(popup_element)
            results.append(el_data)

            webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
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

from time import sleep
from sys import platform
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import subprocess


class ContextElementIterator:
    """utility class used to iterate over element lists that can have elements
    that move in and out of context"""

    def __init__(self, browser, logging, selector, maxlen=1000):
        self.browser = browser
        self.logging = logging
        self.selector = selector
        self.maxlen = maxlen

    def __iter__(self):
        # reset the iterators
        self.__previously_found_element = None
        self.__previous_idx = 0
        return self

    def __next__(self):
        self.element_list = self.selector()
        # self.logging.info("el list len {}".format(len(self.element_list)))

        # is this the first element
        if self.__previous_idx == 0 and len(self.element_list) > 0:
            # return the first el in this list if there are elements
            self.__previously_found_element = self.element_list[0]
            self.__previous_idx = 1
            return self.__previously_found_element
        else:
            self.__previous_idx += 1
            # is the index is within the list and below the max len the return next element
            if (
                self.__previous_idx < len(self.element_list)
                and self.__previous_idx < self.maxlen
            ):
                self.__previously_found_element = self.element_list[self.__previous_idx]
                return self.__previously_found_element
            else:
                raise StopIteration

    def __next_broke__(self):
        self.element_list = self.selector()
        self.logging.info("el list len {}".format(len(self.element_list)))
        element_is_found = False

        if self.__previously_found_element is None and len(self.element_list) > 0:
            self.__previously_found_element = self.element_list[0]
            element_is_found = True
        else:
            list_counter = 0
            if self.__previously_found_element is not None:
                self.logging.info(
                    "   searching for: {}".format(self.__previously_found_element)
                )
            for idx, element in enumerate(self.element_list):
                self.logging.info("looping : {}".format(idx))
                self.logging.info("   checking: {}".format(element))

                list_counter += 1
                if element_is_found:
                    self.__previously_found_element = element
                    self.logging.info("breaking on new element")
                    break
                if element == self.__previously_found_element:
                    self.logging.info("element found")
                    element_is_found = True
                if list_counter > self.maxlen:
                    self.logging.info("max len exceeded")
                    element_is_found = False
                    break
        if not element_is_found:
            self.logging.info("not element is found")
            raise StopIteration
        else:
            self.logging.info("returning")
            return self.__previously_found_element


class PageWrapper:
    """Utility class wrapping up some useful and reusable selenium code"""

    def __init__(self, browser, logging):
        self.browser = browser
        self.logging = logging

    def force_continious_scroll(self, scroll_count=5, sleep_time=3):
        """Try to scroll to bottom of the page and force progressive loading.
        Be careful using this, if you load a lot of elements onto a page
        then try to iterate over them they will often leave the page context
        """
        for scroll_counter in range(scroll_count):
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            # sleep for a bit
            sleep(sleep_time)

    def wait_for_class(self, classname, timeout=10):
        """Wait for an element of the given css class to appear on the page"""

        found_element = WebDriverWait(self.browser, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, classname))
        )

        return found_element

    def find_element_by_text(self, search_text):
        selector = "//*[text()[contains(.,'{}')]]".format(search_text)
        # selector = "//*[contains(text(), '{}')]".format(search_text)
        els = self.browser.find_elements_by_xpath(selector)
        print("--[")
        print(selector)
        print(els)
        print("]--")
        if len(els) > 0:
            return els[0]

    def scroll_element_into_view(self, element):
        self.browser.execute_script("arguments[0].scrollIntoView();", element)
        # a small sleep seems to be required here
        sleep(0.5)

    def get_clipboard_contents(self):
        if platform == "linux" or platform == "linux2":
            clipboard_content = subprocess.check_output(["xsel", "--clipboard"])
        elif platform == "darwin":
            clipboard_content = subprocess.check_output(["pbpaste"])
        elif platform == "win32":
            # todo throw an error of fix this :)
            pass

        return clipboard_content

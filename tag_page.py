from sys import sleep


TAG_PAGE_URL = "https://www.instagram.com/explore/tags/{}/"


class TagPage:
    def __init__(self, tag, browser, logging):
        self.browser = browser
        self.tag = tag
        self.logging = logging
        self.logging.info("tagpage init " + self.tag)
        self.get_tag_page()

    def get_tag_page(self):
        self.logging.info("fetching tag page")
        url = TAG_PAGE_URL.format(self.tag)
        self.logging.info(url)
        self.browser.get(url)
        self.logging.info(url)

    def test_load_success(self):
        self.logging.info("testing success")
        # todo this is a placeholder test forg
        return True

    def process_posts(self):
        self.browser
        sleep(10)

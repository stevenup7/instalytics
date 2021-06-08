TAG_PAGE_URL = "https://www.instagram.com/explore/tags/{}/"


class TagPage:
    def __init__(self, tag, browser, log):
        self.browser = browser
        self.tag = tag
        self.log = log.log
        self.log("tagpage init " + self.tag)
        self.get_tag_page()

    def get_tag_page(self):
        self.log("fetching tag page")
        url = TAG_PAGE_URL.format(self.tag)
        self.log(url)

        self.browser.get(url)
        self.log(url)

    def process_posts(self):
        self.browser

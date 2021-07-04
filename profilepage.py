from time import sleep
from pagewrapper import PageWrapper
from pagewrapper import ContextElementIterator

POPUP_ELEMENT_SELECTOR = "div[role='dialog']"
FOLLOWER_SELECTOR = "span.Jv7Aj"
TAG_PAGE_URL = "https://www.instagram.com/{}/followers/"


class ProfilePage(PageWrapper):
    """Loads up a profile page
    does stuff, yet to be detirmined"""

    def __init__(self, profile_id, browser, logging):
        super().__init__(browser, logging)
        self.profile_id = profile_id
        self.fetch_profile_page()

    def fetch_profile_page(self):
        url = TAG_PAGE_URL.format(self.profile_id)
        self.browser.get(url)
        return self.test_load_success()

    def test_load_success(self):
        # todo this is a placeholder test
        return True

    def get_followers(self, max_num=50):
        sleep(2)
        self.logging.info("findiing followers element")
        followers = self.find_element_by_text("followers")
        print(followers)
        followers.click()
        popup_element = self.wait_for_class(POPUP_ELEMENT_SELECTOR)

        sleep(2)
        follower_list = ContextElementIterator(
            self.browser,
            self.logging,
            lambda: popup_element.find_elements_by_css_selector(FOLLOWER_SELECTOR),
            1000,
        )

        for i, follower in enumerate(follower_list):
            print("{}".format(follower.text))
            if i > 3:
                self.scroll_element_into_view(follower_list.element_list[i - 2])
            sleep(2)

    def get_followed(self):
        pass

from time import sleep
import sys

# page element selectors
LOGIN_ELEMENT = "input[name='username']"
PASSWORD_ELEMENT = "input[name='password']"
SUBMIT_ELEMENT = "//button[@type='submit']" # type may be fragile

SUCCESS_ELEMENT = "----"
FAIL_ELEMENT = "-----"


class LoginScreen:

    def __init__(self, browser, log, username, password):
        self.browser = browser
        self.log = log
        log.log("gettin the homepage")
        self.get_home_page()
        log.log("doing login")
        self.success = self.do_login(username, password)


    def get_home_page(self):
        self.browser.get('https://instagram.com')
        return True

    def do_login(self, username, password):
        # ugly --- wait for the page to init propery
        sleep (1)
        # find the elements and fill 'em in

        username_input = self.browser.find_element_by_css_selector(LOGIN_ELEMENT)
        password_input = self.browser.find_element_by_css_selector(PASSWORD_ELEMENT)
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = self.browser.find_element_by_xpath(SUBMIT_ELEMENT)
        self.log.log("clicking login");
        login_button.click()
        sleep(1)
        self.log.log("login done")
        return True

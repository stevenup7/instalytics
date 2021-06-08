from selenium import webdriver
import config

# screen handlers
from login_screen import LoginScreen
from tag_page import TagPage

import logging

# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)


# setup the webdriver
def init_webdriver():
    browser = webdriver.Firefox()
    return browser


def get_instagram_and_login(browser, log):
    login_screen = LoginScreen(
        browser, log, config.user["username"], config.user["password"]
    )
    return login_screen.success


#  run all the things
if __name__ == "__main__":
    browser = init_webdriver()
    logging.log("loggging in")
    if get_instagram_and_login(browser, logging):
        acrotags = TagPage("acroyoga", browser, logging)
        # done so clean up
        browser.close()
        logging.log("exit success")

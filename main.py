from selenium import webdriver
import config
from time import sleep

# screen handlers
from login_screen import LoginScreen
from profilepage import ProfilePage
from tag_page import TagPage

import logging


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
    if not config.logging["toscreen"]:
        logging.basicConfig(
            filename=config.logging["filename"],
            encoding="utf-8",
            level=config.logging["level"],
        )
    else:
        logging.basicConfig(level=config.logging["level"])

    logging.info("logging in")
    if get_instagram_and_login(browser, logging):
        # need a pause here for login to work
        sleep(2)

        # acrotags = TagPage(
        #     config.analyse["tagpage"], config.analyse["numposts"], browser, logging
        # )

        account = ProfilePage(config.account["account"], browser, logging)
        account.get_followers()
        # account.get.followed()
        # done so clean up
        browser.close()
        logging.info("exit success")

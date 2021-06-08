from selenium import webdriver
import config

# screen handlers
from login_screen import LoginScreen
from tag_page import TagPage

# logging (must be a nice std python one (find it)
from logger import Logger


# setup the webdriver
def init_webdriver():
    browser = webdriver.Firefox()
    return browser


def get_instagram_and_login(browser, log):
    login_screen = LoginScreen(
        browser, log, config.user['username'], config.user['password'])
    return login_screen.success


#  run all the things
if __name__ == '__main__':
    log = Logger()
    browser = init_webdriver()
    log.log("loggging in")
    if get_instagram_and_login(browser, log):
        acrotags = TagPage('acroyoga', browser, log)
        # done so clean up
        browser.close()
        log.log("exit success")

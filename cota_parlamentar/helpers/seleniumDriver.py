from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import os
import gzip

from seleniumwire import webdriver  # Import from seleniumwire

def custom(req, req_body, res, res_body):
    if not req.path or not "recaptcha" in req.path:
        return
    if not res.headers.get("Content-Type", None) == "text/javascript":
        return
    if res.headers["Content-Encoding"] == "gzip":
        del res.headers["Content-Encoding"]
        res_body = gzip.decompress(res_body)
    return res_body + wrapper_code

class TemplateDriver:

    def __init__(self, delay_period = 1):
        self.delay_period = delay_period
        self.startDriver()

    def startDriver(self):

        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", os.path.join(os.getcwd(), 'data/siconfi/tmp'))
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")
        self.driver = webdriver.Firefox(
            firefox_profile=profile,
            )
        self.actionChains = ActionChains(self.driver)
        wait = WebDriverWait(self.driver, 0.1)

    def closeDriver(self):
        self.driver.close()
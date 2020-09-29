import os
import shutil
from pathlib import Path
import json

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from helpers.seleniumDriver import TemplateDriver

import pandas as pd

import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import requests

class OpsDriver(TemplateDriver):

    def getSecretariesListUrls(self):
        self.driver.get("https://ops.net.br/deputado-federal/secretario")
        secretary_urls = []
        while True:
            time.sleep(self.delay_period)
            next_button = self.driver.find_element_by_class_name('paginate_button.page-item.next')
            view_elms = self.driver.find_elements_by_class_name('btn.btn-primary.btn-sm')
            for el in view_elms:
                secretary_urls.append(el.get_attribute('href') )
            next_button.click()
            if 'disabled' in next_button.get_attribute("class"):
                break
        return secretary_urls

    def getAllSecretaries(self):
        secretary_urls = self.getSecretariesListUrls()
        df = pd.DataFrame()
        first = True
        for url in secretary_urls:
            self.driver.get(url)
            time.sleep(self.delay_period)
            self.getSecretaryList().to_csv('./data/Secretarios.csv', mode='a', header=first)
            first = False

    def getSecretaryList(self):
        name_elem = self.driver.find_element(By.XPATH, '//h3[contains(@class,"page-title")]//a')
        name_elem = name_elem.text

        talbe_elms = self.driver.find_elements(By.XPATH, '//table')

        df = pd.DataFrame()

        for table_el in talbe_elms:
            spec_names = ['Parlamentar'] + [el.text for el in table_el.find_elements_by_xpath('.//th')]
            all_specs = []
            for i, row in enumerate(table_el.find_elements_by_xpath(".//tr")):
                item_els = row.find_elements_by_xpath('.//td')
                if len(item_els)>0:
                    try:
                        specs = [name_elem, item_els[0].find_element_by_xpath('./a').text]
                        [specs.append(el.text) for el in item_els[1:]]
                        all_specs.append(specs)
                    except:
                        print('ERROR ON {} TABLE {}'.format(name_elem, i))
            df = df.append(pd.DataFrame(all_specs, columns = spec_names))

        next_buttons = self.driver.find_elements_by_class_name('paginate_button.page-item.next')
        for next_button in next_buttons:
            if 'disabled' not in next_button.get_attribute("class"):
                print('ESSE AQUI TEM MAIS!!!!!!!!!', name_elem)

        return df

if __name__ == '__main__':
    ops_driver = OpsDriver()
    ops_driver.getAllSecretaries()
    ops_driver.closeDriver()
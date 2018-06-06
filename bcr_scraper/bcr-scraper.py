# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd

class BrowserInstance:

    def __init__(self):
        self.web_driver = webdriver.Firefox(executable_path='../geckodriver/geckodriver', log_path='../geckodriver/gecko.log')


class Results:


    def load_results(self):

        print('\nStart: Loading results page for ' + self.year)
        self.browser_instance.web_driver.get(self.url_path)
        elem = self.browser_instance.web_driver.find_element_by_tag_name("body")
        elem.send_keys(Keys.TAB)

        pagedowns = 1000

        while pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

            pagedowns -= 1

            if pagedowns % 100 == 0:
                print(str(pagedowns) + ' left')

        print('\nCompleted: Results page loaded for ' + self.year)

    def scrape_results(self):

        print('\nStart: Scraping results for ' + self.year)
        self.html = self.browser_instance.web_driver.page_source
        self.soup = BeautifulSoup(self.html, 'lxml')

        place = []
        male = []
        female = []
        nr = []
        first_name = []
        last_name = []
        ak_place = []
        ak = []
        teamname = []
        netto = []
        company = []
        header = ['place', 'male', 'female', 'nr', 'first_name', 'last_name', 'ak_place', 'ak', 'teamname', 'netto', 'company']

        def scrape_table(table):

            for tr in table.find_all('tr', class_='table-body'):
                if tr.find(class_='data-entry-table mobile-table'):
                    continue
                cells = tr.findAll('td')

                place.append(cells[0].find(text=True))
                male.append(cells[1].find(text=True))
                female.append(cells[2].find(text=True))
                nr.append(cells[3].find(text=True))
                first_name.append(cells[4].find(text=True))
                last_name.append(cells[5].find(text=True))
                ak_place.append(cells[6].find(text=True))
                ak.append(cells[7].find(text=True))
                teamname.append(cells[8].find(text=True))
                netto.append(cells[9].find(text=True))
                company.append(cells[10].find(text=True))

            df = pd.DataFrame([place, male, female, nr, first_name, last_name, ak_place, ak, teamname, netto, company])
            df = df.transpose()
            df.columns = header

            return df

        self.result_data = scrape_table(self.soup)
        print('\nCompleted: Scraping results for ' + self.year)
        print('\nOutput: Found data for ' + str(self.result_data.shape[0]) + ' runners')

    def save_results_to_csv(self):

        self.result_data.to_csv('../output/company_run_data_' + self.year + '.csv', sep=';', index=False, encoding='utf-8')

        print('\nSaved results to csv')


    def __init__(self, year, url_path):

        self.browser_instance = BrowserInstance()
        self.year = year
        self.url_path = url_path
        self.load_results()
        self.scrape_results()
        self.save_results_to_csv()

"""

some comment stuff
beautiful soup immnowelt.de
extract links and crawl pagination

"""

import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
from random import randint
from selenium import webdriver
import logging
import csv
from tqdm import tqdm

#################### Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs/immowelt_hrefs.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logging.debug("test")
#############################

BASELINK = 'https://www.immowelt.de/liste/bl-baden-wuerttemberg/haeuser/kaufen?sort=relevanz'
SEEDLINK = 'https://www.immowelt.de/liste/bl'
SEEDLINK_EXT1 = '/haeuser/kaufen?sort=relevanz'
SEEDLINK_EXT2 = '/haeuser/kaufen?d=true&sd=DESC&sf=RELEVANCE&sp='
# link = SEEDLINK + federalstate + SEEDLINK_EXT2 + int

federal_states = [
    'Baden-Wuerttemberg',
    'Bayern',
    'Berlin',
    'Brandenburg',
    'Bremen',
    'Hamburg',
    'Hessen',
    'Mecklenburg-Vorpommern',
    'Niedersachsen',
    'Nordrhein-Westfalen',
    'Rheinland-Pfalz',
    'Saarland',
    'Sachsen',
    'Sachsen-Anhalt',
    'Schleswig-Holstein',
    'Thueringen'
]
federal_states = [x.lower() for x in federal_states]

# iterlink = 'seite:'  # add site number

def get_sel_soup(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("/snap/bin/chromium.chromedriver", chrome_options=options)
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    logger.debug("got soup for url {}".format(url))
    return soup


def find_hrefs(lst_aditems):
    lst_href = []
    for soup in lst_aditems:
        lst_href.append(soup.find('a')['href'])
    return lst_href


if __name__ == '__main__':
    # get max num pagination
    start_soup = get_sel_soup(BASELINK)

    # pagination wrapper should have ul and each li should have 'pagination item'  with href. last number in href is
    # page id. search for max num in all li

    logger.info("starting to grab links...")

    # make list of hrefs from pages:
    href_lst = []
    for bl_num in tqdm(range(1, len(federal_states))):

        logger.info("now looking through {}".format(federal_states[bl_num-1]))
        start_soup_url = SEEDLINK + '-' + federal_states[bl_num-1] + SEEDLINK_EXT2 + str(1)
        start_soup = get_sel_soup(SEEDLINK + '-' + federal_states[bl_num-1] + SEEDLINK_EXT2 + str(1))

        max_num_pag = int(start_soup.find_all(class_="Button-c3851")[4].get_text())

        logger.info("max number of pages found: {}".format(max_num_pag))
        for iterator in range(1, max_num_pag):
            # url = SEEDLINK + federalstate + SEEDLINK_EXT2 + int
            soup_url = SEEDLINK + '-' +federal_states[bl_num-1] + SEEDLINK_EXT2 + str(iterator) # bl_num starts at 1


            try:
                soup = get_sel_soup(soup_url)
                # tags = soup.find_all(class_="flex-grow-1 display-flex flex-direction-column")

                for element in soup.find_all(class_="EstateItem-1c115"):
                    endpoint = element.find_all("a", href=True)[0]['href']
                    href_lst.append(endpoint)
                    # print(endpoint)
                # print(len(href_lst), iterator)
                # time.sleep(randint(4, 16))
            except:
                logger.critical("chromium exception error")

        #  if iterator % int(0.1 * max_num_pag) == 0 or iterator == max_num_pag:  # safe every 10% or at the end
        timetag = time.strftime("%Y%m%d-%H%M%S")
        filename = 'data_immowelt/hrefs/immowelt_all_hrefs_ads_{foo}.csv'
        filename = filename.format(foo=timetag)

        with open(filename, 'w') as result_file:
            wr = csv.writer(result_file, dialect='excel', delimiter='\t')
            wr.writerow(href_lst)
            logger.info("hrefs saved to file {}".format(filename))

    logger.info("hrefs saved")

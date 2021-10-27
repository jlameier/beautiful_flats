"""

building links from csv list
get soap from site
process soap
add to df
dump df into sqlite3

"""

import csv
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from tqdm import tqdm
import logging
import time
from pathlib import Path
from random import randint, shuffle
import file_cleanup

#################### Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs/immowelt_ads.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

#############################

path_to_linklist = file_cleanup.get_latest_file('/home/jla/dev/beautiful_flats/data_immowelt/hrefs')
baselink = 'https://www.immonet.de'

testlink = Path('https://www.immowelt.de/expose/22c5s5x')


def get_links_from_file(file):
    list_complete_links = []
    csv.field_size_limit(1024 * 1024)
    with open(file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            for link in row:
                list_complete_links.append(link)
    # shuffle links for obfuscation of crawling
    # shuffle(list_complete_links)
    return list(set(list_complete_links))


def get_sel_soup(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("/snap/bin/chromium.chromedriver", options=options)
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup


def extract_info_d(soup, link):
    # core functionality
    # define fields to be extracted and where to find them
    # return dict of object
    # fields to save: link, headline, price, address,date_age ,date_published, num_views, space, num_rooms, level, type,
    # Equipment, long_description
    # todo fields are not filled correctly nor stable
    d_data = {}
    d_data['link'] = link
    try:
        d_data['headline'] = soup.find("h1").get_text()
    except Exception as e:
        d_data['headline'] = ''
        logger.info("headline error at {}".format(link))
        logger.info(e)
    try:
        tag = soup.find_all("div", {'id':'divImmobilie'})[0]
        _result_str = tag.find_all("div", class_="section_content iw_right")[0].get_text()
        d_data['immowelt_id'] = _result_str.split()[1]
        # print(d_data['immowelt_id'])
    except:
        d_data['immowelt_id'] = ''
        logger.info("immowelt_id error at {}".format(link))
    try:
        d_data['price'] = soup.find_all("div", class_="hardfact")[0].get_text().split('\n')[0]
    except:
        d_data['price'] = ''
        logger.info("price error at {}".format(link))
    try:
        d_data['address'] = soup.find_all("div", {'class':'location'})[0].get_text()
        # print(d_data['address'])
    except:
        d_data['address'] = ''
        logger.info("address error at {}".format(link))
    try:
        d_data['build_year'] = soup.find_all("li", class_="ng-star-inserted")[5].get_text().split(' ')[1]
    except:
        d_data['build_year'] = ''
        logger.info("build_year at {}".format(link))
    try:
        d_data['date_found'] = datetime.datetime.today()
    except:
        d_data['date_found'] = ''
        logger.info("datetime error at {}".format(link))
    try:
        d_data['num_rooms'] = soup.find_all("div", {'class':'hardfact rooms ng-star-inserted'})[0].get_text()
    except:
        d_data['num_rooms'] = ''
        logger.info("num_rooms error at {}".format(link))
    try:  # space1 = living space
        d_data['space1'] = soup.find_all("div", class_="hardfact")[1].get_text().split(' ')[1]
        # print(d_data['space1'])
    except:
        d_data['space1'] = ''
        logger.info("space1 error at {}".format(link))
    try:  # space3 = outside space
        d_data['space3'] = soup.find_all("div", class_="hardfact")[3].get_text().split(' ')[1]
    except:
        d_data['space3'] = ''
        logger.info("space3 error at {}".format(link))
    """    
    try:
        d_data['parking_space'] = soup.find_all("div",class_='datalabel')[1].get_text().split(' ')[1]   # todo
    except:
        d_data['parking_space'] = ''
        logger.info("parking_space error at {}".format(link))
    try:
        d_data['energy'] = soup.find_all("energypass-de", class_="ng-star-inserted")[0].get_text()   # todo
    except:
        d_data['energy'] = ''
        logger.info("energy error at {}".format(link))
    try:
        d_data['features'] = soup.find_all("p")[8].get_text()   # todo
    except:
        d_data['features'] = ''
        logger.info("feature error at {}".format(link))
    try:
        d_data['long_description'] = soup.find_all("p")[7].get_text()   # todo
    except:
        d_data['long_description'] = ''
        logger.info("long_description error at {}".format(link))
    try:
        d_data['location_description'] = soup.find_all("p")[11].get_text()   # todo
    except:
        d_data['location_description'] = ''
        logger.info("location_description error at {}".format(link))
    try:
        d_data['other_description'] = soup.find_all("p")[9].get_text()   # todo
    except:
        d_data['other_description'] = ''
        logger.info("other_description error at {}".format(link))
    """
    try:
        d_data['text_info'] = soup.find_all("div", {'id':'divImmobilie'})[0].get_text()
        if not d_data['text_info']:
            print("stop")
    except:
        logger.info("soup could not be saved")
    return d_data


if __name__ == '__main__':

    list_compl_links = get_links_from_file(path_to_linklist)
    beautiful_homes = []
    logger.info("{cnt} beautiful flats found".format(cnt=len(list_compl_links)))
    num_iterations = (len(list_compl_links))

    ### usually this is done by get_soup

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("/snap/bin/chromium.chromedriver", options=options)

    for cnt in tqdm(range(num_iterations)):

        try:

            driver.get(list_compl_links[cnt])
            page_source = driver.page_source
            #page_source = 'https://www.immowelt.de/expose/22mw25t'
            soup = BeautifulSoup(page_source, 'html.parser')
            #beautiful_homes.append(extract_info_d(soup, page_source))
            beautiful_homes.append(extract_info_d(soup, list_compl_links[cnt]))
            # beautiful_homes.append(extract_info_d(get_sel_soup(list_compl_links[cnt]), list_compl_links[cnt]))
        except:
            logger.critical("fuck, selenium.common.exceptions.InvalidArgumentException: Message: invalid argument")
        # time.sleep(randint(5, 20))
        if cnt % 1000 == 0 or cnt == len(list_compl_links):
            timetag = time.strftime("%Y%m%d-%H%M%S")
            filename = '/home/jla/dev/beautiful_flats/data_immowelt/ads/immowelt_all_pd_ads_{foo}.csv'
            filename = filename.format(foo=timetag)
            df = pd.DataFrame(beautiful_homes)
            df.to_csv(filename)
            logger.info("file written to HDD")

            logger.info("resetting webdriver")
            driver.quit()
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            options.add_argument('--headless')
            driver = webdriver.Chrome("/snap/bin/chromium.chromedriver", options=options)
            logger.info("driver has been reset")
    logger.info("All Immowelt ads saved")

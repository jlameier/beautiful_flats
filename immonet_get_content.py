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
from urllib.request import Request, urlopen
import pandas as pd
import time
from tqdm import tqdm
import re
from random import randint, shuffle

path_to_linklist = '/home/jla/dev/beautiful_flats/immonet_all_hrefs_ads_20211006-165339.csv'
baselink = 'https://www.immonet.de'

testlink= baselink + "/angebot/45224700"

def get_links_from_file(file, baselink):
    list_complete_links = []
    csv.field_size_limit(1024 * 1024)
    with open(file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            for link in row:
                list_complete_links.append(baselink + link)
    # shuffle links for obfuscation of crawling
    shuffle(list_complete_links)
    return list(set(list_complete_links))


def get_sel_soup(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("/snap/bin/chromium.chromedriver", chrome_options=options)
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
    d_data = {}
    d_data['link'] = link
    try:
        d_data['headline'] = soup.find("h1").get_text()
    except:
        d_data['headline'] = ''
        print("headline error", link)
    try:
        d_data['immonet_id'] = soup.find_all("p",class_="hidden-print")[0].get_text()
    except:
        d_data['immonet_id'] = ''
        print("id1 error", link)
    try:
        d_data['seller_id'] = soup.find_all("p",class_="hidden-print")[1].get_text()
    except:
        d_data['seller_id'] = ''
        print("id2 error", link)
    try:
        d_data['price'] = soup.find_all("div", {'id': 'priceid_1'})[0].get_text()
    except:
        d_data['price'] = ''
        print("price error", link)
    try:
        d_data['address'] = soup.find_all("p", class_="text-100 pull-left")[0].get_text()
    except:
        d_data['address'] = ''
        print("address error", link)
    try:
        d_data['build_year'] = soup.find_all("div",{"id": "yearbuild"})[0].get_text()
    except:
        d_data['build_year'] = ''
        print("build_year error", link)
    try:
        d_data['date_found'] = datetime.datetime.today()
    except:
        d_data['build_year'] = ''
        print("datetime error. What year is it?!?!?", link)
    try:
        d_data['num_rooms'] = soup.find_all("div",{"id": "equipmentid_1"})[0].get_text()
    except:
        d_data['num_rooms'] = ''
        print("num_rooms error", link)
    try:  # space1 = living space
        d_data['space1'] = soup.find_all("div", {"id": "areaid_1"})[0].get_text()
    except:
        d_data['space1'] = ''
        print("space1", link)
    try:  # space3 = outside space
        d_data['space3'] = soup.find_all("div", {"id": "areaid_3"})[0].get_text()
    except:
        d_data['space3'] = ''
        print("space3 error", link)
    try:
        if soup.find_all("div", {"id": "equipmentid_13"}):
            d_data['parking_space'] = soup.find_all("div", {"id": "equipmentid_13"})[0].get_text()
        else:
            d_data['parking_space'] = ''
    except:
        d_data['parking_space'] = ''
        print("parking_space", link)
    try:
        if soup.find_all("div", {"id": "panel-energy-pass"})[0].get_text():
            d_data['energy'] = soup.find_all("div", {"id": "panel-energy-pass"})[0].get_text()
        else:
            d_data['energy'] = ''
    except:
        d_data['energy'] = ''
        print("energy", link)
    try:
        d_data['features'] = soup.find_all("div", {"id": "panelFeatures"})[0].get_text()
    except:
        d_data['features'] = ''
        print('features', link)
    try:
        d_data['long_description'] = soup.find_all("div", {"id": "panelObjectdescription"})[0].get_text()
    except:
        d_data['long_description'] = ''
        print("long_description", link)
    try:
        d_data['location_description'] = soup.find_all("div", {"id": "panelLocationDescription"})[0].get_text()
    except:
        d_data['location_description'] = ''
        print('location_description', link)
    try:
        d_data['location_description'] = soup.find_all("div", {"id": "panelOther"})[0].get_text()
    except:
        d_data['location_description'] = ''
        print('location_description', link)
    return d_data

"""
list_compl_links = get_links_from_file(path_to_linklist, baselink)
testlink = 'https://www.immonet.de/angebot/44609159'
beautiful_homes = []
print("{cnt} beautiful flats found".format(cnt=len(list_compl_links)))
#soup = get_sel_soup(list_compl_links[5])
soup = get_sel_soup(testlink)
beautiful_homes.append(extract_info_d(get_sel_soup(list_compl_links[5]), list_compl_links[5]))
print(beautiful_homes)

"""

if __name__ == '__main__':

    list_compl_links = get_links_from_file(path_to_linklist, baselink)
    beautiful_homes = []
    print("{cnt} beautiful flats found".format(cnt=len(list_compl_links)))
    num_iterations = (len(list_compl_links))
    for cnt in tqdm(range(num_iterations)):
        try:
            beautiful_homes.append(extract_info_d(get_sel_soup(list_compl_links[cnt]), list_compl_links[cnt]))
        except:
            print("fuck, selenium.common.exceptions.InvalidArgumentException: Message: invalid argument")
        #time.sleep(randint(5, 20))
        #print(" ", cnt, " / ", len(list_compl_links) )
        if cnt % 1000 == 0 or cnt == len(list_compl_links):
            timetag = time.strftime("%Y%m%d-%H%M%S")
            filename = 'immonet_all_pd_ads_{foo}.csv'
            filename = filename.format(foo=timetag)
            df = pd.DataFrame(beautiful_homes)
            df.to_csv(filename)
            print("file written to HDD")

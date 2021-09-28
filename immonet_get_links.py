"""

some comment stuff
beautiful soup immnonet.de
extract links and crawl pagination

Plan for immonet:
soup main page for selling houses (then flats)
	get max num pagination
	get object ids for each ad "angebotnr"
	assemble href/links
	return list of links
iterate until max num pagination

"""

import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
from random import randint
from selenium import webdriver
import re
import csv

seedlink = 'https://www.immonet.de/'
seedlink_ext1 = 'haus-kaufen.html'
seedlink_ext2 = 'wohnung-kaufen.html'
baselink = 'https://www.immonet.de/immobiliensuche/sel.do?parentcat=2&objecttype=1&pageoffset=1&locationname=Wo:%20Ort%20oder%20PLZ%20oder%20Stadtteil&listsize=26&suchart=1&sortby=0&marketingtype=1&page='
page2link = 'https://www.immonet.de/immobiliensuche/sel.do?parentcat=2&objecttype=1&pageoffset=1&locationname=Wo:%20Ort%20oder%20PLZ%20oder%20Stadtteil&listsize=26&suchart=1&sortby=0&marketingtype=1&page=2'


# iterlink = 'seite:'  # add site number


def get_soup(url):
    req = Request(seedlink, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, features="html.parser")
    return soup


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


def get_pages(seedlink, baselink, maxcount):
    dict_soup_ads = {}
    req = Request(seedlink, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, features="html.parser")
    list_of_site_ads = soup.findAll(class_="aditem")
    dict_soup_ads[1] = list_of_site_ads
    # yield soup
    # next_page = soup.select("a.forward")
    for n in range(2, maxcount):
        next_page = baselink.format(foo=str(maxcount - n))
        req = Request(next_page, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, features="html.parser")
        list_of_site_ads = soup.findAll(class_="aditem")
        dict_soup_ads[n] = list_of_site_ads
        print(len(list_of_site_ads), next_page)
        time.sleep(randint(2, 30))

    tmp = []
    for key in dict_soup_ads:
        tmp.append(dict_soup_ads[key])
    return [item for sublist in tmp for item in sublist]  # flatten the list


def find_hrefs(lst_aditems):
    lst_href = []
    for soup in lst_aditems:
        lst_href.append(soup.find('a')['href'])
    return lst_href


if __name__ == '__main__':
    # get max num pagination
    # baselink = seedlink + seedlink_ext1
    start_soup = get_sel_soup(baselink + str (1))

    # pagination wrapper should have ul and each li should have 'pagination item'  with href. last number in href is page id. search for max num in all li
    max_num_pag = int(start_soup.find_all(class_="pagination-item")[4].get_text())

    # make list of hrefs from pages:
    href_lst = []
    for iterator in range(1,max_num_pag):
        soup = get_sel_soup(baselink + str(iterator))
        #tags = soup.find_all(class_="flex-grow-1 display-flex flex-direction-column")

        for element in soup.find_all("a", onclick=True, href=True):
            endpoint = element['href']
            href_lst.append(endpoint)
            # print(endpoint)
        print(len(href_lst), iterator)
        #time.sleep(randint(4, 16))

        if iterator % int(0.1*max_num_pag) == 0 or iterator == max_num_pag:  # safe every 10% or at the end
            timetag = time.strftime("%Y%m%d-%H%M%S")
            filename = 'immonet_all_hrefs_ads_{foo}.csv'
            filename = filename.format(foo=timetag)

            with open(filename, 'w') as result_file:
                wr = csv.writer(result_file, dialect='excel', delimiter='\t')
                wr.writerow(href_lst)


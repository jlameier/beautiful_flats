"""

building links from csv list - done
get soap from site - done
process soap -done
add to df - done
dump df into sqlite3
todo filter for multiple instances of the same link - done

"""

import csv
import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import time
import re, logging
from glob import glob
from random import randint, shuffle
from tqdm import tqdm
import file_cleanup

#################### Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs/ebay_ads.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logging.debug("test")
#############################

# get hrefs
"""
# todo this can be done way better. just get latest file and be happy. 
href_file = glob(os.getcwd()+"/data_ebay/hrefs/*.csv")
if len(href_file) == 0 or len(href_file) > 1:
    logger.critical("none or more then one href files found. critical error. aborting")
else:
    path_to_linklist = href_file[0]
    BASELINK = 'https://www.ebay-kleinanzeigen.de'

"""

path_to_linklist = file_cleanup.get_latest_file('/home/jla/dev/beautiful_flats/data_ebay/hrefs')
BASELINK = 'https://www.ebay-kleinanzeigen.de'

def get_links(file, baselink):
    logger.info("starting to get links from file...")
    list_complete_links = []
    csv.field_size_limit(1024 * 1024)
    with open(file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            for link in row:
                list_complete_links.append(baselink + link)
    # shuffle links for obfuscation of crawling
    shuffle(list_complete_links)
    logger.info("links ready")
    return list(set(list_complete_links))


def get_soup(url):
    # mimic a real browser
    # return soap object
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, features="html.parser")
    return soup


def extract_info_d(soup, link):
    # core functionality
    # define fields to be extracted and where to find them
    # save them into TODO tbd
    # return something
    # fields to save: link, headline, price, address, date_published, num_views, space, num_rooms, level, type,
    # Equipment, long_description
    d_data = {}
    d_data['link'] = link
    try:
        d_data['headline'] = soup.find(itemprop="name").get_text()
    except:
        d_data['headline'] = 0
        logger.info("headline error at{}".format(link))
    try:
        d_data['price'] = soup.find(id="viewad-price").get_text()
    except:
        d_data['price'] = ''
        logger.info("price error at {}".format(link))
    try:
        d_data['address'] = soup.find(itemprop="locality").get_text()
    except:
        d_data['address'] = ''
        logger.info("address error at".format(link))
    try:
        d_data['published'] = soup.find("div", id="viewad-extra-info").get_text()[1:11]
    except:
        d_data['published'] = ''
        logger.info("published error at {}".format(link))
    try:
        d_data['num_views'] = soup.find(id="viewad-cntr-num").get_text()  # TODO returns empty ??
    except:
        d_data['num_views'] = ''
        logger.info("num_views error at {}".format(link))
    try:
        d_data['id'] = soup.find("div", {"id": "viewad-extra-info"}).text[28::]
    except:
        d_data['id'] = ''
        logger.info("id error at {}".format(link))
    try:
        d_data['space'] = soup.find_all(class_="addetailslist--detail--value")[0].get_text()
    except:
        d_data['space'] = ''
        logger.info("space error at {}".format(link))
    try:
        d_data['num_rooms'] = soup.find_all(class_="addetailslist--detail--value")[1].get_text()
    except:
        d_data['num_rooms'] = ''
        logger.info("num_rooms error at {}".format(link))
    try:
        d_data['level'] = soup.find_all(class_="addetailslist--detail--value")[2].get_text()
    except:
        d_data['level'] = ''
        logger.info("level error at {}".format(link))
    try:
        d_data['type'] = soup.find_all(class_="addetailslist--detail--value")[3].get_text()
    except:
        d_data['type'] = ''
        logger.info("type error at {}".format(link))
    # d_data['furnishing'] = soup.find_all(id='viewad-configuration')
    try:
        # d_data['furnishing'] = soup.find_all(class_="checktag")  # todo make list
        d_data['furnishing'] = [x.text for x in soup.find_all(class_="checktag")]  # todo - done
    except:
        d_data['furnishing'] = ''
        logger.info("furnishing error at {}".format(link))
    try:
        d_data['long_description'] = soup.find(id='viewad-description-text').get_text()
    except:
        d_data['long_description'] = ''
        logger.info("long_description error at {}".format(link))
    try:
        d_data['len_description'] = len(re.findall(r'\w+', d_data['long_description']))
    except:
        d_data['len_description'] = ''
        logger.info("length description error at {}".format(link))
    return d_data


list_compl_links = get_links(path_to_linklist, BASELINK)



beautiful_flats = []
logger.info("{cnt} beautiful flats found".format(cnt=len(list_compl_links)))
logger.info("starting to extract information from soup")

for cnt in tqdm(range(len(list_compl_links))):
    beautiful_flats.append(extract_info_d(get_soup(list_compl_links[cnt]), list_compl_links[cnt]))
    time.sleep(randint(5, 10))
    if cnt % 100 == 0 or cnt == len(list_compl_links):
        timetag = time.strftime("%Y%m%d-%H%M%S")
        filename = 'all_pd_ads_{foo}.csv'
        filename = filename.format(foo=timetag)
        df = pd.DataFrame(beautiful_flats)
        df.to_csv('data_ebay/ads/' + filename)
        logger.info("ads have been saved to file at {}".format(filename))
logger.info("soup has been eaten")

"""
link = "https://www.ebay-kleinanzeigen.de/s-anzeige/eigentumswohnung/1839253138-196-5681"
soup = get_soup(link)
test = extract_info_d(soup, link)
print(test)
"""

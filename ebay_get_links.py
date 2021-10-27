"""

some comment stuff
first of: beautiful soup ebay kleinanzeigen
make list of pages - done
get infos
make df
dump df to sqlite3
use pricing estimation
be happy
never look at it again

"""

import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
from random import randint
import csv
import logging
from tqdm import tqdm


#################### Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs/ebay_href.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logging.debug("test")
#############################

seedlink = 'https://www.ebay-kleinanzeigen.de/s-wohnung-kaufen/wohnung-haus/k0c196'
baselink = 'https://www.ebay-kleinanzeigen.de/s-wohnung-kaufen/seite:{foo}/wohnung-haus/k0c196'


# iterlink = 'seite:'  # add site number


def get_pages(seedlink, baselink, maxcount):
    dict_soup_ads = {}
    req = Request(seedlink, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, features="html.parser")
    list_of_site_ads = soup.findAll(class_="aditem")
    dict_soup_ads[1] = list_of_site_ads
    #yield soup
    # next_page = soup.select("a.forward")
    for n in tqdm(range(2, maxcount)):
        next_page = baselink.format(foo=str(maxcount-n))
        req = Request(next_page, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, features="html.parser")
        list_of_site_ads = soup.findAll(class_="aditem")
        dict_soup_ads[n] = list_of_site_ads
        logger.debug('{} href found at site {}'.format(len(list_of_site_ads), next_page))
        time.sleep(randint(3, 12))

    tmp = []
    for key in dict_soup_ads:
        tmp.append(dict_soup_ads[key])
    return [item for sublist in tmp for item in sublist]  # flatten the list

def find_hrefs(lst_aditems):
    lst_href = []
    for soup in lst_aditems:
        lst_href.append(soup.find('a')['href'])
        logger.debug('href found {}'.format(soup.find('a')['href']))
    return lst_href


if __name__ == '__main__':
    # get all aditem
    all_ads = get_pages(seedlink, baselink, 50)
    # extract hrefs
    list_hrefs = find_hrefs(all_ads)
    href_lst = find_hrefs(all_ads)
    logger.info('number of href found: {}'.format(len(list_hrefs)))
    # print(len(list_hrefs))

    # if iterator % int(0.1 * max_num_pag) == 0 or iterator == max_num_pag:  # safe every 10% or at the end
    timetag = time.strftime("%Y%m%d-%H%M%S")
    filename = 'data_ebay/hrefs/ebay_all_hrefs_ads_{foo}.csv'
    filename = filename.format(foo=timetag)

    with open(filename, 'w') as result_file:
        wr = csv.writer(result_file, dialect='excel', delimiter='\t')
        wr.writerow(href_lst)
        logger.info("hrefs saved to file {}".format(filename))

    logger.info("hrefs saved")

"""
    timetag = time.strftime("%Y%m%d-%H%M%S")
    filename = 'all_hrefs_ads_{foo}.csv'
    filename = filename.format(foo=timetag)
    filepath = "data_ebay"

    with open(filepath + '/' + filename, 'w') as result_file:
        wr = csv.writer(result_file, dialect='excel', delimiter='\t')
        wr.writerow(list_hrefs)
    logger.info('file saved as {}'.format(filename))
"""

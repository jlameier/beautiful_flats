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
import pandas as pd

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
    for n in range(2, maxcount):
        next_page = baselink.format(foo=str(maxcount-n))
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
    # get all aditem
    all_ads = get_pages(seedlink, baselink, 200)
    # extract hrefs
    list_hrefs = find_hrefs(all_ads)
    print(len(list_hrefs))
    timetag = time.strftime("%Y%m%d-%H%M%S")
    filename = 'all_hrefs_ads_{foo}.csv'
    filename = filename.format(foo=timetag)

    with open(filename, 'w') as result_file:
        wr = csv.writer(result_file, dialect='excel', delimiter='\t')
        wr.writerow(list_hrefs)

"""
req = Request('https://www.ebay-kleinanzeigen.de/s-wohnung-kaufen/wohnung-haus/k0c196', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage)
list_of_ads = soup.findAll(class_="aditem")
print(list_of_ads)
"""

"""

building links from csv list - done
get soap from site - done
process soap -done
add to df - done
dump df into sqlite3
todo filter for multiple instances of the same link

"""
import csv
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import time
from random import randint, shuffle


path_to_linklist = '/home/jla/dev/beautiful_flats/all_hrefs_ads_20210721-034310.csv'
baselink = 'https://www.ebay-kleinanzeigen.de'


def get_links(file, baselink):
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
        print(link)
    try:
        d_data['price'] = soup.find(id="viewad-price").get_text()
    except:
        d_data['price'] =''
        print(link)
    try:
        d_data['address'] = soup.find(itemprop="locality").get_text()
    except:
        d_data['address'] =''
        print(link)
    try:
        d_data['published'] = soup.find("div", id="viewad-extra-info").get_text()[1:11]
    except:
        d_data['published'] =''
        print(link)
    try:
        d_data['num_views'] = soup.find(id="viewad-cntr-num").get_text() # TODO returns empty ??
    except:
        d_data['num_views'] =''
        print(link)
    try:
        d_data['id'] = soup.find("div", {"id": "viewad-extra-info"}).text[28::]
    except:
        d_data['id'] = ''
        print(link)
    try:
        d_data['space'] = soup.find_all(class_="addetailslist--detail--value")[0].get_text()
    except:
        d_data['space'] =''
        print(link)
    try:
        d_data['num_rooms'] = soup.find_all(class_="addetailslist--detail--value")[1].get_text()
    except:
        d_data['num_rooms'] = ''
        print(link)
    try:
        d_data['level'] = soup.find_all(class_="addetailslist--detail--value")[2].get_text()
    except:
        d_data['level'] = ''
        print(link)
    try:
        d_data['type'] = soup.find_all(class_="addetailslist--detail--value")[3].get_text()
    except:
        d_data['type'] = ''
        print(link)
    d_data['furnishing'] = soup.find_all(id='viewad-configuration')
    try:
        d_data['furnishing'] = d_data['furnishing'][0].contents[3].text  # todo make list
    except:
        d_data['furnishing'] = ''
        print(link)
    try:
        d_data['long_description'] = soup.find(id='viewad-description-text').get_text()
    except:
        d_data['long_description'] =''

    return d_data

list_compl_links = get_links(path_to_linklist,baselink)
# create dataframe and add dict from extract_info to df todo this comes later. first of: make list of all soups/returns (list of dics) and then convert to df
# df = pd.DataFrame(index=range(len(list_compl_links)), columns= list(d_data.keys()))

beautiful_flats = []
print("{cnt} beautiful flats found".format(cnt=len(list_compl_links)))
for cnt in range(len(list_compl_links)):
    beautiful_flats.append(extract_info_d(get_soup(list_compl_links[cnt]),list_compl_links[cnt]))
    time.sleep(randint(2, 10))
    print(cnt)
    if cnt % 50 == 0:
        timetag = time.strftime("%Y%m%d-%H%M%S")
        filename = 'all_pd_ads_{foo}.csv'
        filename = filename.format(foo=timetag)
        df = pd.DataFrame(beautiful_flats)
        df.to_csv(filename)



# now drop the df to a

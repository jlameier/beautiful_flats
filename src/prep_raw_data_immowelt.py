# some tools to prepare raw data from csv and clean them to be imported by a datamodel or at least processed

from src import ads_loader
import re
import numpy as np
import decimal
import locale
import math
import typing
from matplotlib import pyplot as plt

locale.setlocale(locale.LC_NUMERIC, 'de_DE.utf8')

immowelt_dat_lst = ads_loader.load_ads_files_dir('/home/jla/dev/beautiful_flats/data_immowelt/final')
immowelt_dat_df = ads_loader.concat_df(immowelt_dat_lst)

print(immowelt_dat_df.head())

def get_price(pricelist: list) -> list:
    # gets list, makes elements into int, returns list
    list_return = []
    for item in pricelist:
        if item:
            try:
                string_value = re.findall(r'\d+', item)
                if string_value:
                    string_value = ''.join(string_value)
                    #    string_value = string_value[0]+string_value[1]
                    num_value = int(string_value)
                    if ',' in item:
                        # print("comma found")
                        num_value = 0.01*num_value
                    list_return.append(num_value)
                    # list_return.append(num_value)
                else:
                    list_return.append(np.nan)
            except TypeError:
                # print("Typeerror, added nan")
                # print(item)
                list_return.append(num_value)
    return list_return


def get_postid(postidlist: list) -> list:
    # this will be a bit of pain, since the information seems to jump wildly.
    # first attempt: split string at " " and look for substrings of length 5

    list_return = []
    for element in postidlist:
        #### from here on we analyze the content of the field
        # if string, we can split it. otherwise check for float
        if isinstance(element, str):
            # check if five numbers
            try:
                string_value = re.findall(r'\d+', element)  # returns list
                if len(string_value) > 0:  # if list not empty
                    if len(string_value[0]) == 5:
                        num_value = int(string_value[0])
                        if num_value > 999 and num_value < 99999:
                            list_return.append(num_value)
                        else:
                            list_return.append(np.nan)
                    else:
                        list_return.append(np.nan)
                else:
                    list_return.append(np.nan)
            except TypeError:
                # print("Typeerror, added nan")
                # print(item)
                list_return.append(np.nan)
        else:
            list_return.append(np.nan)
    return list_return


def get_space(spacelist: list) -> list:  # todo if interpunction in function, last part is cut off 1.800 -> 1.ß
    # handle three cases: no punctuation, comma and dot
    list_return = []
    numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)

    for item in spacelist:
        if item:
            print(item)
            try:
                num_value = float(rx.findall(item)[0])
                list_return.append(num_value)
                print(num_value)
                """
                string_value = re.findall(r'\d+', item)
                if len(string_value) > 1:
                   string_value = ''.join(string_value)
                   #    string_value = string_value[0]+string_value[1]
                   num_value = int(string_value[0])
                   list_return.append(num_value)
                else:
                   num_value = int(string_value[0])
                   list_return.append(np.nan)
                """
            except TypeError:
                print("TypeError at " , item)
                list_return.append(np.nan)
            except IndexError:
                print("index problem at ", item)
                list_return.append(np.nan)
            except ValueError:
                print("valueerror at ", item)
                list_return.append(np.nan)
        else:
            list_return.append(np.nan)
    return list_return


def prep_immowelt(df_raw):
    # returns a dataframe with cleaned data
    # so far only price, space, id and address ready to go
    # df = df_raw.dropna()
    #print(df_raw.head())
    # d_clean = dict()
    # d = dict.fromkeys(
    #    ['link', 'headline', 'price', 'post_io', 'published', 'num_views', 'ebay_id', 'space_in', 'space_out',
    #     'num_rooms', 'level', 'furnishing', 'long_description'])
    df_raw['price'] = get_price(df_raw['price'])
    df_raw['space1'] = get_price(df_raw['space1'])  # todo using getprice instead of space, dangerous, please revert
    df_raw['space3'] = get_space(df_raw['space3'])
    df_raw['address'] = get_postid(df_raw['address'])
    # conversion to int not for NA/inf
    # df_raw.astype({'id': int,'price': int,'space': int,'address': int})
    df_ready = df_raw
    return df_ready

# testinput_postid = ['60322 b alblabalbla', 'hier isteht  gar nichts haste gehört', 'ahahaha 1.600 nad93982nsjh', 'hefshef 06123']
# testpostid = get_postid(testinput_postid)
test_post_ID = 0
df= prep_immowelt(immowelt_dat_df)
print("done")

# rudimentory filters:

df = df[df['price'] < 10000000]
# df = df[df['address'] > 60308]
# df = df[df['address'] < 65936]

df = df[df['address'] > 950]
df = df[df['address'] < 99999]

post_codes = sorted(set(df['address']))

eurpm_flat = {}
for element in post_codes:
    matching_ids = df[df['address'] == element]
    lst_price_postid = []
    lst_machting_ids = matching_ids['address']
    for flat_id in lst_machting_ids.index:
        lst_price_postid.append(df.loc[flat_id]['price']/df.loc[flat_id]['space1'])
        if df.loc[flat_id]['price']/df.loc[flat_id]['space1'] < 50000:
            eurpm_flat[element] = sum(lst_price_postid) / len(lst_price_postid)
        else:
            print("strange eur / sqm")
            print("price:", df.loc[flat_id]['price'], "space1:", df.loc[flat_id]['space1'])
            df.drop(flat_id, inplace=True)


df.to_csv('data_for_dask.csv')
print('data_saved')
"""
target_var = df['price']
plot1 = plt.figure(1)
colors = list("rgbcmyk")
plt.scatter(eurpm_flat.keys(), eurpm_flat.values(), color=colors.pop())
# plt.scatter(df['address'], target_var)
plt.xlabel('plz')
plt.ylabel('ppm²')
plt.grid()
"""
"""
plot2 = plt.figure(2)
plt.scatter(df['space1'], target_var)
plt.xlabel('space ')
plt.ylabel('price')
"""
plt.show()
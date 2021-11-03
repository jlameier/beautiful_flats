# some tools to prepare raw data from csv and clean them to be imported by a datamodel or at least processed

from src import ads_loader
import re
import numpy as np
import math
import typing

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


def get_space(spacelist: list) -> list:
    list_return = []
    for item in spacelist:
        if item:
            try:
                string_value = re.findall(r'\d+', item)
                if string_value:
                    #string_value = ''.join(string_value)
                    #    string_value = string_value[0]+string_value[1]
                    num_value = int(string_value[0])
                    list_return.append(num_value)
                else:
                    list_return.append(np.nan)
            except TypeError:
                # print("Typeerror, added nan")
                # print(item)
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
    df_raw['space1'] = get_space(df_raw['space1'])
    df_raw['space3'] = get_space(df_raw['space3'])
    df_raw['address'] = get_postid(df_raw['address'])
    # conversion to int not for NA/inf
    # df_raw.astype({'id': int,'price': int,'space': int,'address': int})
    df_ready = df_raw
    return df_ready

# testinput_postid = ['60322 b alblabalbla', 'hier isteht  gar nichts haste gehört', 'ahahaha 1.600 nad93982nsjh', 'hefshef 06123']
# testpostid = get_postid(testinput_postid)
test_post_ID = 0
test= prep_immowelt(immowelt_dat_df)
print("done")
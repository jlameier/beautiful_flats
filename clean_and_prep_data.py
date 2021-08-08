"""

load df
transform text and prices, to decimals
clear empties
make new df containing ID, price, space, rooms, level, number furnishing
save df

"""

import pandas as pd
import re
import numpy as np

df = pd.read_csv("all_pd_ads_20210807-195436.csv")

# remove column views and kill lines with NaN
df = df.drop(columns='num_views')
df = df.dropna()

# convert to numbers
df['price'] = df['price'].astype(str)

# convert prices to  int
def get_price_int(df):
    list_return = []
    for index, row in df.iterrows():
        obj_value = row['price']
        string_value = re.findall(r'\d+', obj_value)
        if string_value:
            string_value = ''.join(string_value)
        #    string_value = string_value[0]+string_value[1]
            num_value = int(string_value)
            if num_value > 10000000:
                list_return.append(np.nan)
            else:
                list_return.append(num_value)
            # list_return.append(num_value)
        else:
            list_return.append(np.nan)
    return list_return


def get_space_int(df):
    list_return = []
    for index, row in df.iterrows():
        obj_value = row['space']
        string_value = re.findall(r'\d+', obj_value)
        if string_value:
            #string_value = ''.join(string_value)
            #    string_value = string_value[0]+string_value[1]
            num_value = int(string_value[0])
            list_return.append(num_value)
        else:
            list_return.append(np.nan)
    return list_return


def get_rooms_int(df):
    list_return = []
    for index, row in df.iterrows():
        obj_value = row['num_rooms']
        string_value = float(obj_value.replace(',', '.'))
        list_return.append((string_value))
    return list_return


def get_level_int(df):
    list_return = []
    for index, row in df.iterrows():
        obj_value = row['level']
        string_value = re.findall(r'\d+', obj_value)
        if string_value:
            string_value = ''.join(string_value)
            num_value = int(string_value)
            if num_value > 100:
                list_return.append(np.nan)
            else:
                list_return.append(num_value)
        else:
            list_return.append(np.nan)
    return list_return


def get_num_furnishing(df):
    list_return = []
    for index, row in df.iterrows():
        obj_value = row['furnishing']
        string_values = obj_value.split('\n')
        if string_values:
            test= len(list(filter(None, string_values)))
            list_return.append(len(list(filter(None, string_values))))
        else:
            list_return.append(np.nan)
    return list_return

def get_postid_int(df):
    list_return = []
    for index, row in df.iterrows():
        obj_value = row['address']
        string_value = re.findall(r'\d+', obj_value)
        if string_value:
            string_value = ''.join(string_value)
            num_value = int(string_value)
            if num_value < 100 or num_value > 99999:
                list_return.append(np.nan)
            else:
                list_return.append(num_value)
        else:
            list_return.append(np.nan)
    return list_return


# construct df from transformed values
d_num = {}
d_num['furnishing'] = get_num_furnishing(df)
d_num['level'] = get_level_int(df)
d_num['price'] = get_price_int(df)
d_num['id'] = df['id']
d_num['rooms'] = get_rooms_int(df)
d_num['space'] = get_space_int(df)
d_num['postID'] = get_postid_int(df)
d_num['words'] = df['len_description']


df_num = pd.DataFrame(d_num)
df_num = df_num.dropna()

# check distribution and parameter correlation - check for dependency between variables

df_num.to_csv('num_items_clean.csv')
print("done")

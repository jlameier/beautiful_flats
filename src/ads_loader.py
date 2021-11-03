# provide loadding methods. likely for single files as well as directories
import pandas as pd
from pathlib import Path


def load_ads_file(fpath):
    df = pd.read_csv(fpath)
    return df


def load_ads_files_dir(dir_path):
    # returns list of dataframes from path
    lst_files_p = Path(dir_path).glob('*/')
    lst_df = []
    for f_name in lst_files_p:
        lst_df.append(pd.read_csv(f_name))
    return lst_df


def concat_df(lst_df):
    # append dataframes. attention: TODO if columnames mismatch, this will fail
    df = pd.concat(lst_df, ignore_index=True)
    return df


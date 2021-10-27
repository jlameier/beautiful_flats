"""

provides some useful functions to delete safes and move files and so on. to be expanded

"""
from pathlib import Path
import os, glob
from typing import List, Optional
import logging

#################### Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs/file_cleanup.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

#############################

def get_latest_file(path):
    # returns latest file in a folder
    # directory = pathlib.Path(__file__).parent.resolve()
    # path_to_file = max(Path(path).glob('*/'), key=os.path.getmtime)

    try:
        path_to_file = max(Path(path).glob('*/'), key=os.path.getmtime)
        try:
            logger.debug("latest file {} found".format(path_to_file))
        except:
            logger.debug("no file found")
        return path_to_file
    except:
        logger.debug("no file found")


def delete_file(file):
    # expects pathobject to file
    # tested - ok
    try:
        if file:
            os.remove(file)
    except:
        logger.debug("file not found to delete")
    return None


def delete_all_but_file(path, filename):
    # tested - ok
    files = list(path.glob('*.csv'))
    try:
        files.remove(filename)
        for f in files:
            os.remove(f)
        logger.debug("successfully removed {} files from {}".format(len(files)-1),path)
    except:
        print('delete_all_but_one_file: no such file {} in path {}'.format(filename,path))




def clear_dir(path: object):
    # tested - ok
    # be careful. only use on lowest level tier
    path = Path(path)
    files = path.glob('*.csv')
    for f in files:
        os.remove(f)

"""
path_cwd = os.getcwd()
test = get_latest_file(Path(path_cwd + '/data_ebay/hrefs'))
#delete_all_but_file(Path(path_cwd + '/data_ebay/hrefs'), test)
#delete_file(test)
# clear_dir('test')
print(test)
"""
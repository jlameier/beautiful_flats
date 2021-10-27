# this is a routine the manages the saved files from the scraper and deletes duplicates
# final single files should be stored in to folder "final"
import shutil

import file_cleanup
from pathlib import Path
import logging

#################### Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs/file_management.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

#############################

######## ebay ##########

# find latest file in /home/jla/dev/beautiful_flats/data_ebay/ads
p = Path('/home/jla/dev/beautiful_flats/data_ebay/ads')
ebay_latest_p = file_cleanup.get_latest_file(p)
# move to final
destination_p = Path('/home/jla/dev/beautiful_flats/data_ebay/final')
try:
    shutil.move(str(ebay_latest_p), str(destination_p))
    logger.info("moving latest ads file from {} to /data_ebay/final".format(ebay_latest_p))
except:
    logger.warning("no file in ads")

# delete href and duplicate ads
file_cleanup.clear_dir(Path('/home/jla/dev/beautiful_flats/data_ebay/hrefs'))
logger.info("cleaned up hrefs for ebay")
file_cleanup.clear_dir(Path('/home/jla/dev/beautiful_flats/data_ebay/ads'))
logger.info("cleaned up ads for ebay")
######## immonet ########

# find latest file in /home/jla/dev/beautiful_flats/data_ebay/ads
p = Path('/home/jla/dev/beautiful_flats/data_immonet/ads')
immonet_latest_p = file_cleanup.get_latest_file(p)
# move to final
destination_p = Path('/home/jla/dev/beautiful_flats/data_immonet/final')
try:
    shutil.move(str(immonet_latest_p), str(destination_p))
    logger.info("moving latest ads file from {} to /data_immonet/final".format(immonet_latest_p))
except:
    logger.warning("no file in ads")

# delete href and duplicate ads
file_cleanup.clear_dir(Path('/home/jla/dev/beautiful_flats/data_immonet/hrefs'))
logger.info("cleaned up hrefs for immonet")
file_cleanup.clear_dir(Path('/home/jla/dev/beautiful_flats/data_immonet/ads'))
logger.info("cleaned up ads for immonet")

######## immowelt ########

# find latest file in /home/jla/dev/beautiful_flats/data_ebay/ads
p = Path('/home/jla/dev/beautiful_flats/data_immowelt/ads')
immowelt_latest_p = file_cleanup.get_latest_file(p)
# move to final
destination_p = Path('/home/jla/dev/beautiful_flats/data_immowelt/final')
try:
    shutil.move(str(immowelt_latest_p), str(destination_p))
    logger.info("moving latest ads file from {} to /data_immowelt/final".format(immowelt_latest_p))
except:
    logger.warning("no file in ads")

# delete href and duplicate ads
file_cleanup.clear_dir(Path('/home/jla/dev/beautiful_flats/data_immowelt/hrefs'))
logger.info("cleaned up hrefs for immowelt")
file_cleanup.clear_dir(Path('/home/jla/dev/beautiful_flats/data_immowelt/ads'))
logger.info("cleaned up ads for immowelt")
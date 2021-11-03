#!/bin/bash

source /home/jla/dev/venvs/beautiful_flats/bin/activate

python ebay_get_links.py &
python immonet_get_links.py &
python immowelt_get_links.py &
wait
# python file_management.py &
wait 
python ebay_get_content.py &
python immonet_get_content.py &
python immowelt_get_content.py &

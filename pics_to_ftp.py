#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This script pushes an export file and all new pictures of the Store audit to the external FTP Server.

- **Parameters**

    None

- **Examples**

:Example:

python pics_to_ftp.py

--> Runs the script:)


"""


import sys
import os
from SQL_module import *
from transformations_module import *
from transfer_module import *
from datetime import *


ts = datetime.today().strftime("%Y-%m-%d__%H-%M")
# Specify the log name
logname = "logs/Store-Audit__" + ts + ".log"
logging.basicConfig(filename=logname, level=logging.DEBUG)

# in testmode, a test FTP-Server is used
testmode = False

# the FTP settings are stored in environment variables
if testmode:
    host = os.environ['TEST_HOST']
    user = os.environ['TEST_USER']
    pw = os.environ['TEST_PW']
else:
    host = os.environ['PROD_HOST']
    user = os.environ['PROD_USER']
    pw = os.environ['PROD_PW']

ftp = ftplib.FTP(host)
ftp.set_pasv(False)
ftp.login(user, pw)


# CHANGE the Check id for which the results will be fetched
data = execute_query(task_results_query("5"))
assert all(s for s in data[0]), "Store Type is empty, but should contain store id"
assert len(old_export.columns) == len(data.columns), "Column length mismatch"

# name all the audit elements (appears in picture file name)
data.columns = ["Audit-Element_1", "Audit-Element_2", "Audit-Element_3", "Audit-Element_4", "Audit-Element_5"]

# the colums of the dataframe that contain the photo steps
# this should not change
photo_cols = [5, 6, 8, 10, 12, 14, 18, 20, 22, 24, 26, 28, 31]

# extract the store ID from the type column
data = get_store_id(data)

data = dataframe_to_unicode(data)

down_counter = 0
up_counter = 0

# UPLOAD the pictures
if not testmode:
    for i in photo_cols:
        # create new file names in matching column
        # CHANGE the name of the wave (will be part of the file name)
        matching_table = create_new_filenames(data, i, "Wave-1")
        logging.debug("matching table for Wave-1 column %s created. table contains %s links." % (i, len(matching_table.index)))

        # check which pictures have been uploaded already and delete those links
        remaining = delete_duplicate_links(matching_table, ftp)
        logging.debug("%s links remaining for column %s" % (len(remaining.index), i))

        # download the remaining pictures and upload them to the FTP
        down_counter, up_counter = transfer_all_pics(remaining, ftp, down_counter, up_counter)

# UPLOAD the export
fname = os.path.join("Exports", "Store-Audit_" + str(datetime.today().date()) + ".tab")

if not os.path.isdir(os.path.dirname(fname)):
    os.makedirs(os.path.dirname(fname))

# export to CSV; client expects tab delimited
data.to_csv(fname, sep="\t", index=False, encoding="utf-8")

# upload export file to FTP
upload_file(ftp, fname)

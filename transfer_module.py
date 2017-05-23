#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the methods to download the pictures and to transfer them to the FTP server."""


import sys
import os
import pandas as pd
import numpy as np
import urllib2
import urllib
import requests
import shutil
import ftplib
import logging


def transfer_picture(url, fname, folder, ftp, down_counter, up_counter):
    """Retrieve a picture from url and save it at fname"""

    if folder not in ftp.nlst():
        ftp.mkd(folder)

    ftp.cwd(folder)

    r = urllib.urlopen(url)
    code = r.getcode()
    logging.debug('Picture %s:\nCode %s' % (url, code))
    if code == 200:
        down_counter += 1
        print("File " + url + " successfully downloaded")
        logging.info("File " + fname + " successfully downloaded")
        try:
            # upload to ftp
            ftp.storbinary("STOR " + fname, r, 1024)
            up_counter += 1
            print("File number: " + str(up_counter) + " -- " + fname + " successfully uploaded to directory " + folder)
            logging.info("File number: " + str(up_counter) + " -- " + fname + " successfully uploaded to directory " + folder)
        except:
            print("ERROR occured while uploading %s" % fname)
            logging.error("ERROR occured while uploading %s" % fname)
            sys.exit(1)
    else:
        print "ERROR: " + str(code)

    ftp.cwd("..")

    return down_counter, up_counter


def transfer_all_pics(data, ftp, down_counter, up_counter):
    """read links to pictures, download and rename them"""

    folder = data.columns.values[0]

    for i in data.index:
        link = data.ix[i, 0]
        fname = data.ix[i, 1]
        down_counter, up_counter = transfer_picture(link, fname, folder, ftp, down_counter, up_counter)

    return down_counter, up_counter


def upload_file(ftp, fname):
    """uploads a file to an ftp server"""

    dir = os.path.dirname(fname)
    file = os.path.basename(fname)

    if dir not in ftp.nlst():
        ftp.mkd(dir)

    ftp.cwd(dir)

    ftp.storbinary("STOR " + file, open(fname, "r"), 1024)

    if file in ftp.nlst():
        print("File  -- " + file + " successfully uploaded to directory " + dir)

    else:
        print("ERROR: File " + file + " could NOT be located in directory " + dir)

    ftp.cwd("..")
    return

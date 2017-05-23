#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains functions for transforming the data ebfore tranferring."""

import sys
import os
import pandas as pd
import numpy as np
import shutil
import ftplib
import re
import logging


def create_new_filenames(data, column, wave):
    """assigns a new filename to each picture link"""

    check_question = data.columns.values[column]
    check_question = replace_umlaute(check_question)
    matching_table = []
    logging.debug("Creating new filenames for column number %s i.e. check_question '%s'" % (column, check_question))
    for i in data.index:
        if not pd.isnull(data.ix[i, column]):
            old_fname = str(data.ix[i, column])
            new_fname = wave + "__" + check_question + "__" + str(data.ix[i, 0]) + ".jpg"
            matching_table.append([old_fname, new_fname])

    if len(matching_table) > 0:
        matching_table = pd.DataFrame.from_records(matching_table)
        matching_table.columns = [check_question, "new_name"]
    else:
        matching_table = pd.DataFrame(columns=[check_question, "new_name"])

    return matching_table


def delete_duplicate_links(matching_table, ftp):
    """checks which fotos are already uploaded to ftp and returns the remaining
    list of picture yet to be uploaded"""

    remaining_links = matching_table
    directory = matching_table.columns.values[0]
    if directory in ftp.nlst():
        ftp.cwd(directory)
        files = ftp.nlst()
        remaining_links = matching_table[matching_table["new_name"].isin(files) == False]
        ftp.cwd("..")

    return remaining_links


def replace_umlaute(text):
    """replaces the Umlaute in a string"""

    text = re.sub('ö', 'oe', text)
    text = re.sub('ä', 'ae', text)
    text = re.sub('ü', 'ue', text)
    text = re.sub('Ö', 'Oe', text)
    text = re.sub('Ä', 'Ae', text)
    text = re.sub('Ü', 'Ue', text)
    text = re.sub('ß', 'ss', text)
    return text


regex = re.compile('2[0-9]{8}')
# the shop-ID is a 9-digit number starting with a 2

def get_shop_id(data):
    """retrieves the shop ID from the type field in export"""
    for i in data.index:
        logging.debug("ROW NO %s: Trying to extract shop-ID for store %s from type: %s" % (i, data.ix[i, 0], data.ix[i, 1]))
        buffer = regex.search(data.ix[i, 0])
        assert buffer != None, "No shop id found! Please check Type-Field of store %s" % data.ix[i, 1]
        data.ix[i, 0] = buffer.group(0)

    return data


def dataframe_to_unicode(df):
    """transforms a pandas dataframe into unicode format.
    Necessary for excel export"""

    for i in df.index:
        for j in range(len(df.ix[0])):
            if isinstance(df.ix[i, j], basestring):
                if not isinstance(df.ix[i, j], unicode):
                    df.ix[i, j] = df.ix[i, j].decode('utf-8')
    return df

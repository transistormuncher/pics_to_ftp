#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the methods to interact with the SQL database."""

import sys
import os
import psycopg2
import pandas as pd
import numpy as np


def execute_query(query):
    """This function executes a given SQL query and returns the resulting table
    as a Pandas Data Frame"""

    con = None
    try:
        con = psycopg2.connect(
            # the connection settings are stored in environment variables
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PW'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'])
        cur = con.cursor()
        cur.execute(query)
        results = cur.fetchall()
        rows = list(results)
    except psycopg2.DatabaseError as e:
        print 'Error %s' % e
        sys.exit(1)
    finally:
        if con:
            con.close()
    rows = pd.DataFrame.from_records(rows)
    return rows


def task_results_query(check_id):
    """Returns the relevant check results and picture links"""

    query = """
    SELECT store.category,
    c.store_name,
    c.results_submitted,
    c.text_0[1], c.text_1[1], p.photo_6, p.photo_7,
    c.text_8[1], p.photo_9, c.text_10[1], p.photo_11,
    c.text_12[1], p.photo_13, c.text_14[1], p.photo_15,
    c.text_16[1], c.text_17[1], c.text_18[1], p.photo_19,
    c.text_20[1], p.photo_21, c.text_22[1], p.photo_23,
    c.text_24[1], p.photo_25, c.text_26[1], p.photo_27,
    c.text_28[1], p.photo_29, c.text_30[1], c.text_31[1],
    p.photo_32, c.text_35[1], c.text_33[1], c.text_34[1]

    FROM check_results c INNER JOIN photo_results p ON c.id =
    p.check_id
    INNER JOIN store on c.store_id = store.id
    WHERE c.check_id in (%s)
    ORDER BY c.results_submitted DESC
    %s
    """ % (check_id)
    return query

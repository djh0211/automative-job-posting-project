import psycopg2
import requests
import pandas as pd
from pandasql import sqldf
from tqdm import tqdm
import os
import json

import re
import csv
from datetime import date
import datetime

global key_json_path
key_json_path = "/home/gcpairflow001/env.json"

def get_sql_connection(autocommit : bool):
    global key_json_path
    with open(key_json_path, 'r') as f:
        key_json = json.load(f)
    
    host = key_json["host"]
    user = key_json["user"]
    password = key_json["password"]
    port = key_json["port"]
    dbname = key_json["dbname"]
    conn = psycopg2.connect(f"dbname={dbname} user={user} host={host} password={password} port={port}")
    conn.set_session(autocommit=autocommit)
    return conn

def run_query(sql : str) -> None:
    conn = get_sql_connection(False)
    cur = conn.cursor()

    try:
        cur.execute(sql) 
        conn.commit()  # cur.execute("COMMIT;")와 동일
        res = cur.fetchall()
        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()  # cur.execute("ROLLBACK;")와 동일


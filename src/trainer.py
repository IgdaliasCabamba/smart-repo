import sys
sys.dont_write_bytecode = True

import sqlite3 as db
from typing import Union
import tokenizer
import pathlib
import time
import datetime
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
import rapidfuzz

#import pprint

def train(from_path:str, output_path:str) -> None:
    file_model = f'{output_path}/pypi_model.db'
    datas = tokenizer.normalize(from_path)

    conn = db.connect(file_model)

    conn.execute('''create table if not exists PACKAGES
                (
                    ID                     integer primary key     autoincrement,
                    package_name           text    not     null,
                    package_summary        text    not     null,
                    package_description    text    not     null
                )'''
            )
    conn.commit()

    for data in datas:
        conn.execute(
            f"""
            insert into PACKAGES (package_name, package_summary, package_description)
            VALUES (
                '{data["package_name"]}',
                '{data["package_summary"]}',
                '{data["package_description"]}'
            )
            """
        )
    
    conn.commit()
    conn.close()

def _get_data(model:str, table_name:str, query:str) -> list:
    conn = db.connect(model)

    cursor = conn.execute(f"select {query} from {table_name}")
    data = []
    if query == "*":
        return cursor
    
    for row in cursor:
        data.append(row)

    conn.close()
    return data

def get_all_data():
    init_time = datetime.datetime.now()
    cursor_data = _get_data("models/pypi_model.db", "PACKAGES", "*")
    load_time = datetime.datetime.now()
    data = {
        "packages":[],
        "summaries":[],
        "descriptions":[]
    }
    
    for item in cursor_data:
        data["packages"].append(item[1])
        data["summaries"].append(item[2])
        data["descriptions"].append(item[3])
        if "jedi" in item[3]:
            print(item[3])

    end_time = datetime.datetime.now()
    print(f"Took [{load_time-init_time}] to load all data")
    print(f"Took [{end_time-init_time}] to do all operations\n")

    while True:
        query = input(">>> ")
        if len(query) > 1:
            init_time = datetime.datetime.now()
            results = rapidfuzz.process.extract(query, data["descriptions"], limit=10)
            for result in results:
                print(result)

            print(f"\n\n\n[{len(results)} RESULTS IN : {datetime.datetime.now()-init_time}]")

        else:
            break

get_all_data()
#train(from_path="data_set", output_path="models")
#pprint.pprint(tokenizer.normalize("data_set")[0]["package_description"])
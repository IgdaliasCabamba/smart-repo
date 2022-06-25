import json
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
    data = []
    
    for item in cursor_data:
        data.append(
            {
                "package":item[1],
                "summary":item[2],
                "description":item[3]
            }
        )

    end_time = datetime.datetime.now()
    print(f"Took [{load_time-init_time}] to load all data")
    print(f"Took [{end_time-init_time}] to do all operations\n")

    while True:
        results = []
        query = input(">>> ")
        if len(query) > 1:
            init_time = datetime.datetime.now()
            for item in data:
                x1 = rapidfuzz.fuzz.token_set_ratio(query, item["description"])
                x2 = rapidfuzz.fuzz.QRatio(query, item["description"])
                if x1 > 85 and x2 > 1:
                    results.append(item)

            #results = rapidfuzz.process.extract(query, data["descriptions"], limit=10)

            print(f"\n\n\n[{len(results)} RESULTS IN : {datetime.datetime.now()-init_time}]")
            for res in results:
                print(res["package"])

        else:
            break

def test():
    with open("data_set/pypi_api.data.j.json", "r") as fp:
        x = json.load(fp)
        for y in x.keys():
            if y == "jk-pypiorgapi":
                query = "an for accessing python packet information hosted on pypi org"
                #query = "fetch "
                a = tokenizer.get_clean_text(x[y]["description"])
                print(a,"\n\n")
                #a = x[y]["description"]
                print("ratio:", rapidfuzz.fuzz.ratio(query, a))
                print("partial ratio:", rapidfuzz.fuzz.partial_ratio(query, a))
                print("partial token ratio:", rapidfuzz.fuzz.partial_token_ratio(query, a))
                print("partial ratio alignment:", rapidfuzz.fuzz.partial_ratio_alignment(query, a))
                print("partial token set ratio:", rapidfuzz.fuzz.partial_token_set_ratio(query, a))
                print("partial token sort ratio: ", rapidfuzz.fuzz.partial_token_sort_ratio(query, a))
                
                print("token ratio:", rapidfuzz.fuzz.token_ratio(query, a))
                print("token set ratio:", rapidfuzz.fuzz.token_set_ratio(query, a))
                print("token sort ratio:", rapidfuzz.fuzz.token_sort_ratio(query, a))
                
                print("W ratio:", rapidfuzz.fuzz.WRatio(query, a))
                print("Q ratio:", rapidfuzz.fuzz.QRatio(query, a))
                print(rapidfuzz.utils.default_process(query))
                #use Token set ratio

#train(from_path="data_set", output_path="models")
get_all_data()
#test()
#pprint.pprint(tokenizer.normalize("data_set")[0]["package_description"])
import glob
import os
import json
import re
from cleantext import clean

def get_clean_text(raw_text) -> str:
    clean_text:str = clean(raw_text,
        fix_unicode=True,               # fix various unicode errors
        to_ascii=True,                  # transliterate to closest ASCII representation
        lower=True,                     # lowercase text
        no_line_breaks=True,           # fully strip line breaks as opposed to only normalizing them
        no_urls=True,                  # replace all URLs with a special token
        no_emails=True,                # replace all email addresses with a special token
        no_phone_numbers=True,         # replace all phone numbers with a special token
        no_numbers=True,               # replace all numbers with a special token
        no_digits=True,                # replace all digits with a special token
        no_currency_symbols=True,      # replace all currency symbols with a special token
        no_punct=True,                 # remove punctuations
        replace_with_punct="",          # instead of removing punctuations you may replace them
        replace_with_url=" ",
        replace_with_email=" ",
        replace_with_phone_number=" ",
        replace_with_number=" ",
        replace_with_digit=" ",
        replace_with_currency_symbol="",
        lang="en"                       # set to 'de' for German special handling
    )
    clean_text = re.sub(r'[^_a-z-\s]', '', clean_text)
    return clean_text

def normalize(path:str, files_regex:str="*.json", recursive:bool=False) -> list:
    useful_data = []
    raw_files = glob.glob(os.path.join(path, files_regex), recursive=recursive)
    raw_files = sorted(raw_files)

    for raw_file in raw_files:
        with open(raw_file, "r") as fp:
            raw_data = json.load(fp)
            for name in raw_data.keys():
                desc = get_clean_text(raw_data[name]["description"])
                summ = get_clean_text(raw_data[name]["summary"])
                useful_data.append(
                    {
                        "package_name":name,
                        "package_description":desc,
                        "package_summary":summ
                    }
                )
                #break
                print(f"Processed package: {name}")

        print(f"Processed file: {raw_file}")
        #break
    
    return useful_data

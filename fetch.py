"""
Author: bishwarup
Created: Friday, 17th March 2020 12:18:42 pm
Modified: Friday, 20th March 2020 2:43:27 pm [bishwarup]
"""


import re
from tqdm import tqdm
import requests
import warnings
from bs4 import BeautifulSoup
from collections import defaultdict
import json

all_headers = [
    "State",
    "Confirmed (Indian)",
    "Confirmed (Foreign-Nationals)",
    "Recovered",
    "Death",
]


def get_headers(l):
    headers = []
    for item in l:
        # if item == "S. No.":
        #     headers.append(None)
        if ("State" in item) or ("UT" in item):
            headers.append("State")
        elif "Confirmed" in item:
            if "Indian" in item:
                headers.append("Confirmed (Indian)")
            else:
                headers.append("Confirmed (Foreign-Nationals)")
        elif "Cure" in item:
            headers.append("Recovered")
        elif "Death" in item:
            headers.append("Death")
        else:
            headers.append(None)
    return headers


def get_headers_index(headers):
    def get_index(list_, item):
        try:
            idx = list_.index(item)
        except ValueError:
            idx = None
        return idx

    return [get_index(headers, item) for item in all_headers]


def format_records(date, records):
    def get_elem(list_, idx):
        try:
            return list_[idx]
        except TypeError:
            return "-1"

    r = dict()
    for i, record in enumerate(records[:-1]):
        if i == 0:
            headers = get_headers(record)
            indices = get_headers_index(headers)
        else:
            rec = [int(get_elem(record, k)) for k in indices[1:]]
            r.update({record[indices[0]]: {date: rec}})
    return r


def get_record(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Server unresponsive")
    text = response.text
    soup = BeautifulSoup(text, "lxml")
    table = soup.find(text="S. No.")
    records = []
    try:
        table = table.find_parent("table")
        rows = table.find_all("tr")

        for i, row in enumerate(rows):
            if i == 0:
                header = [col.get_text() for col in row.find_all("th")]
                if len(header) > 0:
                    records.append(header)
            cols = row.find_all("td")
            record = [col.get_text() for col in cols]
            if len(record) > 0:
                records.append(record)
    except AttributeError:
        warnings.warn("Could not locate/parse the table")
    finally:
        return records


def get_date_info(url):
    date = re.search("http(s)?://web.archive.org/web/(\d+)/.*", url).group(2)[:8]
    return date[6:] + "/" + date[4:6] + "/" + date[:4]


def get_stats(urls):
    records = dict()
    for url in tqdm(urls):
        s = get_record(url)
        date = get_date_info(url)
        # print(date)
        record = format_records(date, s)
        # print(record)
        for k, v in record.items():
            if k in records.keys():
                # print("here")
                records[k].update(record[k])
            else:
                records[k] = record[k]
    return records


if __name__ == "__main__":
    url = "https://web.archive.org/web/20200310105744/https://www.mohfw.gov.in/"
    urls = [
        "https://web.archive.org/web/20200310105744/https://www.mohfw.gov.in/",
        "https://web.archive.org/web/20200312234030/https://www.mohfw.gov.in/",
        "https://web.archive.org/web/20200313153014/https://www.mohfw.gov.in/",
        "https://web.archive.org/web/20200314175115/https://www.mohfw.gov.in/",
        "https://web.archive.org/web/20200315232553/https://www.mohfw.gov.in/",
        "https://web.archive.org/web/20200316145236/https://www.mohfw.gov.in/",
        "http://web.archive.org/web/20200317050937/https://www.mohfw.gov.in/",
        "https://web.archive.org/web/20200318233345/https://www.mohfw.gov.in/",
        "https://web.archive.org/web/20200319155059/https://www.mohfw.gov.in/",
    ]
    r = get_stats(urls)
    with open("history.json", "w") as f:
        json.dump(r, f)

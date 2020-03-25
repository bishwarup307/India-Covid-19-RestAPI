"""
Author: bishwarup
Created: Friday, 17th March 2020 3:24:31 pm
Modified: Friday, 20th March 2020 2:42:57 pm [bishwarup]
"""
import os
import re
from bs4 import BeautifulSoup
import requests
from fetch import get_record, format_records
from datetime import datetime, timedelta
import time
import logging
import json
import argparse
import bmemcached

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s:%(levelname)s:%(name)s:%(processName)s:%(message)s"
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# TODO: remove multiple dependency on save
class Update:
    def __init__(self, url):
        self.url = url
        self._total_cases = 168
        self._last_updated = datetime.now()
        self.db = bmemcached.Client(
            os.environ.get("MEMCACHEDCLOUD_SERVERS").split(","),
            os.environ.get("MEMCACHEDCLOUD_USERNAME"),
            os.environ.get("MEMCACHEDCLOUD_PASSWORD"),
        )
        history = self.db.get("history")
        if history is None:
            with open("history.json", "r") as f:
                history = json.load(f)
            self.db.set("history", history)

    @property
    def total_cases(self):
        return self._total_cases

    @total_cases.setter
    def total_cases(self, value):
        if value > self.total_cases:
            self._total_cases = value

    @property
    def last_updated(self):
        return self._last_updated

    @last_updated.setter
    def last_updated(self, value):
        if isinstance(value, datetime):
            self._last_updated = value

    def get_last_modified(self):
        resp = requests.get(self.url)
        if resp.status_code == 200:
            last_modified = resp.headers["last-modified"]
            last_modified = datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S %Z")
        else:
            logger.error(f"cannot connect to server: {self.url}")
            last_modified = None
        return last_modified

    def _needs_update(self):
        last_snapshot = self.db.get("last_snapshot")
        if last_snapshot is None:
            return True

        if isinstance(last_snapshot, str):
            last_snapshot = datetime.strptime(last_snapshot, "%d/%m/%Y %H-%M-%S")

        last_modified = self.get_last_modified()

        if last_modified is None:
            logger.info(
                "Coudn't fetch details from server, trying to serve cached results..."
            )
            return False

        if last_modified <= last_snapshot:
            return False
        return True

    def get_overall(self):
        history = self.update()
        confirmed = sum([sum(list(v.items())[-1][1][:2]) for k, v in history.items()])
        recovered = sum([list(v.items())[-1][1][2] for k, v in history.items()])
        death = sum([list(v.items())[-1][1][3] for k, v in history.items()])

        return {
            "Confirmed": confirmed,
            "Recovered": recovered,
            "Death": death,
        }

    def update(self):
        history = self.db.get("history")
        if history is None:
            logger.critical("Coudn't access database...")
            raise
        if self._needs_update():
            record = get_record(self.url)
            record = format_records(
                datetime.strftime(datetime.now(), "%d/%m/%Y"), record
            )
            for k, _ in record.items():
                if k in history.keys():
                    history[k].update(record[k])
                else:
                    history[k] = record[k]
            self.db.set("history", history)
            self.db.set("last_snapshot", datetime.now().strftime("%d/%m/%Y %H-%M-%S"))
            logger.info("updated history...")
        return history

    # def run(self, waiting=60):
    #     while True:
    #         total_cases = self._check_for_update()
    #         if total_cases > self.total_cases:
    #             self._update()
    #             self.last_updated = datetime.now()
    #             self.total_cases = total_cases
    #         else:
    #             print(
    #                 "{}: records not updated yet, will check again in {:.2f} hr.".format(
    #                     datetime.now().strftime("%d/%m/%Y %H-%M-%S"), waiting / 3600
    #                 )
    #             )
    #         time.sleep(waiting)


if __name__ == "__main__":

    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "-t",
    #     "--waiting",
    #     type=int,
    #     default=60,
    #     help="waiting time for the next check (in seconds)",
    # )
    # args = vars(parser.parse_args())
    update = Update("https://www.mohfw.gov.in/")
    overall = update.get_overall()
    overall["timestamp"] = (datetime.now() - timedelta(days=3)).strftime(
        "%d/%m/%Y %H-%M-%S"
    )
    with open("overall.json", "w") as f:
        json.dump(overall, f)
    # update.run(args["waiting"])

import logging
import os
import shutil
import time
from datetime import datetime
from typing import Any

import schedule
from dotenv import dotenv_values

__ORIGIN_PATH = "/origin"
__TARGET_PATH = "/target"

def log(msg: str, logger: Any=logging.info):
    time: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    logger(f"[{time}]  {msg}")

def clean_folder(origin: str, target: str):
    for file in os.listdir(target):
        origin_path = os.path.join(origin, file)
        target_path = os.path.join(target, file)

        if not os.path.exists(origin_path):
            if os.path.isdir(target_path):
                shutil.rmtree(target_path)
            elif os.path.isfile(target_path):
                os.remove(target_path)
        elif os.path.isdir(target_path):
            clean_folder(origin_path, target_path)

def copy_folder(origin: str, target: str):
    for file in os.listdir(origin):
        origin_path = os.path.join(origin, file)
        target_path = os.path.join(target, file)

        if os.path.isdir(origin_path):
            copy_folder(origin_path, target_path)
        elif os.path.isfile(origin_path):
            if not os.path.exists(target):
                os.makedirs(target)
            if not os.path.exists(target_path) or (os.path.getmtime(origin_path) > os.path.getmtime(target_path)):
                shutil.copy2(origin_path, target_path)

def copy_all():
    log("Copying ...")
    # shutil.copy2(__ORIGIN_PATH, __TARGET_PATH)
    copy_folder(__ORIGIN_PATH, __TARGET_PATH)
    log("Cleaning ...")
    clean_folder(__ORIGIN_PATH, __TARGET_PATH)
    log("Done!")


if __name__ == "__main__":
    # setup
    logging.basicConfig(level="DEBUG")
    log("Setup ...")
    if not os.path.exists(__ORIGIN_PATH):
        os.makedirs(__ORIGIN_PATH)
    if not os.path.exists(__TARGET_PATH):
        os.makedirs(__TARGET_PATH)

    # config
    config = dotenv_values("/.env")
    log(f"Configuration ({len(config)}):")
    for key, value in config.items():
        log(f"{key}={value}")

    # scheduler loop
    log("Starting...")
    copy_all()
    schedule.every(int(config["HOURS_GAP"])).hours.at(config["TIME_START"], config["TIME_ZONE"]).do(copy_all)
    while True:
        schedule.run_pending()
        time.sleep(10)
import logging
import os
import shutil
import threading
import time
from datetime import datetime
from threading import BoundedSemaphore
from typing import Any

import schedule
from dotenv import dotenv_values

__ORIGIN_PATH = "/origin"
__TARGET_PATH = "/target"
__SEMAPHORE = None

def seconds_to_str(seconds: float):
    if seconds < 1:
        return f"{int(seconds*1000)}ms"
    else:
        minutes = 0
        while seconds >= 60:
            minutes += 1
            seconds -=60
        if minutes == 0:
            return f"{int(seconds*1000)/1000.}sec"
        return f"{minutes}min {int(seconds*1000)/1000.}sec"

def log(msg: str, logger: Any=logging.info) -> None:
    time: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    logger(f"[{time}]  {msg}")

def clean_folder(origin: str, target: str) -> None:
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

def copy_files(origin: str, target: str) -> None:
    folder_threads = []

    for file in os.listdir(origin):
        origin_path = os.path.join(origin, file)
        target_path = os.path.join(target, file)

        if os.path.isdir(origin_path):
            thread = threading.Thread(target=copy_files, args=(origin_path, target_path))
            folder_threads.append(thread)
            thread.start()

        elif os.path.isfile(origin_path):
            if not os.path.exists(target_path) or (os.path.getmtime(origin_path) > os.path.getmtime(target_path)):
                with __SEMAPHORE:
                    shutil.copy2(origin_path, target_path)

    for thread in folder_threads:
        thread.join()

def copy_folders(origin: str, target: str) -> None:
    count = 0
    if not os.path.exists(target):
        os.makedirs(target)
        count += 1
    for file in os.listdir(origin):
        origin_path = os.path.join(origin, file)
        if os.path.isdir(origin_path):
            count += copy_folders(origin_path, os.path.join(target, file))
    return count

def copy_all():
    log("Full copy started.")
    full_start = time.time()

    log("Cleaning ...")
    start = time.time()
    clean_folder(__ORIGIN_PATH, __TARGET_PATH)
    end = time.time()
    log(f"Done. Took {seconds_to_str(end - start)}")

    log("Copying folders ...")
    start = time.time()
    copy_folders(__ORIGIN_PATH, __TARGET_PATH)
    end = time.time()
    log(f"Done. Took {seconds_to_str(end - start)}")

    log("Copying files (threaded) ...")
    start = time.time()
    copy_files(__ORIGIN_PATH, __TARGET_PATH)
    end = time.time()
    log(f"Done. Took {seconds_to_str(end - start)}")

    full_end = time.time()
    log(f"Full copy done in {seconds_to_str(full_end - full_start)} !")


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")

    # config
    config = dotenv_values("/.env")
    log(f"Configuration ({len(config)}):")
    for key, value in config.items():
        log(f"{key}={value}")

    # setup
    log("Setup ...")
    if not os.path.exists(__ORIGIN_PATH):
        os.makedirs(__ORIGIN_PATH)
    if not os.path.exists(__TARGET_PATH):
        os.makedirs(__TARGET_PATH)
    __SEMAPHORE = BoundedSemaphore(value=int(config["NBR_THREADS"]))

    # scheduler loop
    log("Starting...")
    copy_all()
    schedule.every(int(config["HOURS_GAP"])).hours.at(config["TIME_START"], config["TIME_ZONE"]).do(copy_all)
    while True:
        schedule.run_pending()
        time.sleep(10)
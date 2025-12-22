
# 📂 BackupScheduler

A lightweight, automated folder synchronization tool designed for low-power devices. It ensures your target directory is a perfect mirror of your origin directory by copying new/edited files and removing deleted ones.

[![Docker Hub](https://img.shields.io/badge/Docker_Hub-Repository-blue?logo=docker)](https://hub.docker.com/r/chades/backupscheduler)
[![GitHub](https://img.shields.io/badge/GitHub-Source_Code-lightgrey?logo=github)](https://github.com/ChadEstoupStreiff/BackupScheduler)


## ✨ Features
* 🔄 **One-way Mirroring:** Keeps target perfectly synced with origin.
* 🕒 **Smart Scheduling:** Run backups during off-peak hours to save resources.
* 🍓 **Pi-Optimized:** Designed specifically for low-power servers like Raspberry Pi.
* 🧵 **Multithreading:** Configurable thread count to speed up transfers (best for SSDs).
* 🐳 **Docker Ready:** Easy deployment via Docker Compose.


## 🤔 Why use this?
While a **NAS** or **RAID** setup provides better real-time data redundancy, they can be resource-intensive or expensive. 

**BackupScheduler is ideal for:**
* **Low-Power Hardware:** If you run a Nextcloud instance on a Raspberry Pi, you don't want a backup process slowing down your UI during the day.
* **Energy Efficiency:** CPU and Disk usage only spike during your scheduled window (e.g., the middle of the night).
* **Simplicity:** No complex RAID controllers needed—just a simple copy-paste logic.


## ⚙️ Configuration

Create a `.env` file in your project directory. Use the following template:

```toml
# ==== PATHS ====
# Ensure these match the volume mounts in your docker-compose
ORIGIN_PATH="/home/user/data"
TARGET_PATH="/mnt/external_drive/backup"

# ==== SCHEDULER ====
HOURS_GAP=24
TIME_ZONE="Europe/Paris" # Find yours: [https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)
TIME_START="02:00"

# ==== PERFORMANCE ====
NBR_THREADS=1 # Increase for SSDs, keep at 1 for HDDs to prevent clicking/wear

```

## 🚀 How to Launch

### 1. Prepare Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: '3'

services:
  backup_scheduler:
    image: chades/backupscheduler:latest
    container_name: backup_scheduler
    restart: always
    env_file:
      - .env
    volumes:
      - ${ORIGIN_PATH}:/origin
      - ${TARGET_PATH}:/target
      - .env:/.env

```

*(Check [Docker Hub Tags](https://hub.docker.com/r/chades/backupscheduler/tags) for specific versions.)*

### 2. Start the Service

Run the following command:

```bash
docker-compose up -d
```

> ⚠️ WARNING ⚠️  
> **Initial Sync:** The application starts a full copy immediately upon container launch. The first run will be resource-intensive depending on your data size. Subsequent runs will be much faster as only changes are synced.

## 🛠️ Requirements

* Docker & Docker Compose
* Source and Target directories with appropriate read/write permissions.

# BackupScheduler
Simple app to copy and paste all folder from origin to target.  
This app will search new or edited file and copy it to the target folder. Then it will delete files in target that are missing in origin.   
This job is executed every X time based on configuration file.  
#### [Docker Hub Repository](https://hub.docker.com/r/chades/backupscheduler)  
#### [Source code](https://github.com/ChadEstoupStreiff/BackupScheduler)  

## Why use this instead of a NAS or RAID disks ?
Buy a NAS or configure RAID on your disks if you can, it's way more secure for your data.  
The advantage of this backup scheduler is that it only copy whenever you want. That means you can configure to copy in the middle of the night. It consume disk and CPU power only when you want, it's very usefull for powerless servers like raspberries.  
This application was created to create a disk copy of a disk who handle a nextcloud instance on a raspberry. Not enought power means to do some tricks.


## Configuration
Create and edit .env file.
```toml
#====PATH====
ORIGIN_PATH="/home/chad/dev"
TARGET_PATH="/home/dev_copy"

#====SCHEDULER====
HOURS_GAP=24
TIME_ZONE="Europe/Paris" # https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
TIME_START="22:25"

#====OTHER====
NBR_THREADS=1 # Speed up copy, not recommended on HDD disks
```
## How to launch
Launch by starting docker container with docker-compose.  
**!Beware! This will start a copy when you start the container, it can be a heavy processus and can reduce your server performance temporarly.**  
The first copy is way more heavy than next ones.  
### Docker-compose YAML
```YAML
version: '3'

services:
  backup_scheduler:
    env_file:
      - .env
    image: chades/backupscheduler:<VERSION>
    container_name: backup_scheduler
    restart: always
    volumes:
      - ${ORIGIN_PATH}:/origin
      - ${TARGET_PATH}:/target
      - .env:/.env
```
[See versions here.](https://hub.docker.com/r/chades/backupscheduler/tags)  
Launch docker-compose with command:
> docker-compose up -d
# BackupScheduler
Simple app to copy and paste all folder from origin to target.  
This app will search new or edited file and copy it to the target folder. Then it will delete files in target that are missing in origin.   
This job is executed every X time based on configuration file.

## Why use this instead of a NAS or a RAID disks ?
Buy a NAS or configure RAID on your disks if you can, it's way more secure for your data.  
The advantage of this backup scheduler is that it only copy whenever you want. That means you can configure to copy in the middle of the night. It consume disk and CPU power only when you want, it's very usefull for powerless servers like raspberries.  
This application was created to create a disk copy of a disk who handle a nextcloud instance on a raspberry. Not enought power means to do some tricks.


## Configuration
Copy .env_ex file.
> cp .env_ex .env

Edit .env file.
```toml
#====PATH====
ORIGIN_PATH="/tmp/origin"
TARGET_PATH="/tmp/target"

#====SCHEDULER====
HOURS_GAP=24
TIME_ZONE="Europe/Paris" # https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
TIME_START="22:25"
```
## How to launch
Launch by starting docker container with docker-compose.  
**!Beware! This will start a copy when you start the container, it can be a heavy processus and can reduce your server performance temporarly.**  
The first copy is way more longer than next ones.  
> docker-compose up -d
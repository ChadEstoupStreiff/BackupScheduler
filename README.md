# BackupScheduler
Simple app to copy and paste all folder from origin to target.  
This app will search new or edited file and copy it to the target folder. Then it will delete files in target that are missing in origin.   
This job is executed every X time based on configuration file.


## Configuration
Copy .env_ex file
> cp .env_ex .env

Edit .env file
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
Launch by launching docker container with docker-compose
> docker-compose up -d
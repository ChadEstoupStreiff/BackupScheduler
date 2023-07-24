VERSION=$(cat VERSION)
sudo docker build -t chades/backupscheduler:$VERSION .
sudo docker push chades/backupscheduler:$VERSION
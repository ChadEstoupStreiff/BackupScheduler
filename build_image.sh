VERSION=$(cat VERSION)
docker build -t chades/backupscheduler:$VERSION .
docker push chades/backupscheduler:$VERSION
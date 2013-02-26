#!/usr/bin/env bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

cd $DIR
source ./venv/bin/activate
# TODO read options from command line
echo "Run api server on 8080..."
#nohup gunicorn --bind 0.0.0.0:8080 --worker-class gevent --workers 2 groupapis > /dev/null 2>&1 &
nohup python groupapis.py > /dev/null 2>&1 &
echo "Run websocket server on 8082..."
#nohup gunicorn --bind 0.0.0.0:8082 --worker-class gevent --workers 2 liveapis > /dev/null 2>&1 &
nohup python liveapis.py > /dev/null 2>&1 &

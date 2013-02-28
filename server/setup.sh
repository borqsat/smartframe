#!/usr/bin/env bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
cd $DIR

VENV='venv'
BOOTSTRAP='bootstrap.py'

#curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
# create bootstrap.py
python create-venv-script.py
# create virtualenv
python $BOOTSTRAP $VENV
rm $BOOTSTRAP

echo "Virtual environment set-up finished!"
echo "----------------------------------------------------------------------"
echo -e "Please run \e[0;36m'. ./$VENV/bin/activate'\e[0m to switch to virtual python env."
echo "----------------------------------------------------------------------"


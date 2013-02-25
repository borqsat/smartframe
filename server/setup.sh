#!/usr/bin/env bash

VENV='venv'
BOOTSTRAP='bootstrap.py'

#curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
python create-venv-script.py
python $BOOTSTRAP $VENV
rm $BOOTSTRAP

echo "Virtual environment set-up finished!"
echo "----------------------------------------------------------------------"
echo "Please run '. ./$VENV/bin/activate' to switch to virtual python env."
echo "----------------------------------------------------------------------"


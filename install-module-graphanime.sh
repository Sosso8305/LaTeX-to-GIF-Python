#!/bin/bash

echo "Installation of module graphanime ...."
source .venv/bin/activate 2> /dev/null
cd graphanime
python setup.py install
cd ..
echo "End Installation"
#!/bin/bash

echo "Installation of module graphanime ...."
.\.venv\Scripts\Activate.ps1
cd graphanime
python setup.py install
cd ..
echo "End Installation"
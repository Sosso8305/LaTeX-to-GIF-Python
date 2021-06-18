#!/bin/bash

# Create virtual environment in .venv folder
echo "Creating virtual environment in .venv folder"
python3 -m venv .venv 

echo "Sourcing virtual environment"
source .venv/bin/activate 2> /dev/null

echo "Installation of requirements.txt"
pip install -r requirements.txt 2> /dev/null
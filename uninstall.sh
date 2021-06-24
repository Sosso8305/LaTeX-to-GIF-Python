#!/bin/bash

echo "deleting...."
source .venv/bin/activate 2> /dev/null

rm -R graphanime/build/
rm -R graphanime/dist/
rm -R graphanime/graphanime.egg-info/

deactivate

rm -R .venv

echo "finish !!!"
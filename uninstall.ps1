echo "deleting...."
source .venv/bin/activate 2> /dev/null

rmdir graphanime/build/ /s
rmdir graphanime/dist/  /s
rmdir graphanime/graphanime.egg-info/ /s

deactivate

rmdir .venv

echo "finish !!!"
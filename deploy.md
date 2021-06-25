# how deloy our module in Pypi
```
cd graphanime
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
rm dist/*
python3 -m twine upload dist/*

user on Pypi

```
# GIF-Dijktra-Python


User
===================
## use module 
install module thanks to /setup.py in local
```
source install-module-graphanime.sh
```
install module thanks to pip and [Pypi](https://pypi.org/project/graphanime/)
```
pip install graphanime
```

then in python :
```py
from graphanime import *

G = load("graph.tex")
animation=Dijkstra(x, "node 1", "node 5")
gen_gif(animation, "myGIF",700)
```
And for more details in [other README](graphanime/README.md)

Dev
====================================================
## Virtual environnement Develop On Linux / MAC
Please make sure you have [Python 3.7](https://www.python.org/) or greater and [pip](https://pypi.org/project/pip/) properly installed
```
apt-get install python3 python3-pip python3-venv -y
```

Then run the following command in the root project folder
```
source install.sh
```

## Virtual environnement Develop On Windows
Please make sure you have [Python 3.7](https://www.python.org/) or greater and [pip](https://pypi.org/project/pip/) properly installed

Then run the script
```
.\install.ps1
```

# For use Venv
on Mac or Linux:
```
source .venv/bin/activate
```

on Windows:
```
.\.venv\Scripts\Activate.ps1
```

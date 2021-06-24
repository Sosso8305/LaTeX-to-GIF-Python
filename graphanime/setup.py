#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import graphanime


setup(

    name='graphanime',
    
    version=graphanime.__version__,

    packages=find_packages(),

    author= "ALTAVILLA Théo / DUPLAN Xavier / EL RAWAS Gaëthan / ZOUAOUI Sofiane / help of INSA CVL",

    author_email = "sofiane.zouaoui@insa-cvl.fr",

    description="create execution graph in GIF/PDF with LaTex",

    long_description=open('./README.md').read(),

    install_requires=["pdf2image==1.16.0","apng==0.3.4"],

    include_package_data=True,

    url='https://github.com/Sosso8305/GIF-Dijkstra-Python',

    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: LaTeX",
        "Natural Language :: French",
        "Operating System :: Linux",
        "Operating System :: Windows",
        "Operating System :: Darwin",
        "Topic :: graph",
        "Topic :: GIF",
        "Topic :: animation",
    ],

    license="MIT Lisence"
)
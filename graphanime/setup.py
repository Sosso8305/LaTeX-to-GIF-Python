#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(

    name='graphanime',
    
    version="0.0.7",

    packages=find_packages(),

    author= "ALTAVILLA Théo / DUPLAN Xavier / EL RAWAS Gaëthan / ZOUAOUI Sofiane / help of INSA CVL",

    author_email = "sofiane.zouaoui@insa-cvl.fr",

    description="create execution graph in GIF/PDF with LaTex",

    long_description=open('./README.md').read(),
    long_description_content_type="text/markdown",

    install_requires=["pdf2image","apng"],

    include_package_data=True,

    url='https://github.com/Sosso8305/LaTeX-to-GIF-Python',

    classifiers=[
        "Programming Language :: Python",
        "Natural Language :: French",
    ],

    license="MIT Lisence"
)
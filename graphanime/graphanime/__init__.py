#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ce module a pour but de générer des GIF, pdf type standalone ou Beamer ou APNG
    a partir d'un graph écrit en LaTeX. Et montrant l'execution d'un algorithme
"""

__version__ = "0.1.0"


from .animation import load, gen_beamer, gen_pdf, gen_apng, gen_gif
from .algorithm import Dijkstra, BellmanFord, FordFulkerson, Kruskal, Floyd_Warshall

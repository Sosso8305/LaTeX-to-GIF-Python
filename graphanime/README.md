Graphanime - create execution graph in GIF/PDF
=================================================

Ce module a pour but de générer des GIF, pdf type standalone ou Beamer ou APNG
a partir d'un graph écrit en LaTeX. Et montrant l'execution d'un algorithme

Install module:
```
pip install graphanime
```

# Commande
## load(file.tex)
return an object Graph which represented graph write in LaTeX

## Dijkstra(graph,source,sink):
excute dijkstra algorithm on graph and return list of graph

## gen_beamer(anim,file)
it's Back-end for slide Beamer with a source is list of graph (anim)

## gen_pdf(anim,file)
it's Back-end for natural pdf with a source is list of graph (anim)

## gen_gif(anim,file)
it's Back-end for GIF with a source is list of graph (anim)

## gen_apng(anim,file)
it's Back-end for APNG with a source is list of graph (anim)
**WARNING**: it's not support everywhere 







# Graphanime - create execution graph in GIF/PDF


This module aim to create GIF, APNG, pdf type standalone or Beamer from a graph 
written in LaTex. And showing an excution of one algorithm (for exemple Dijkstra)

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


# Template

```
\documentclass[tikz]{standalone}

\usepackage{tikz}
\usetikzlibrary{quotes}
%\usepackage{}
%\use...library{}

%\tikzset{every figure} = []
\begin{document}
	\begin{tikzpicture} 
		%\node (name node) at(x,y) [options split by comma] {display} ;
		\node () at(,) [] {} ;
		\node () at(,) [] {} ;
		
%(name node): characters prohibited: ) [ ; \node
%at(x,y): optional : x and y must to do a well coordonate : numbers 
%[options split by comma]:  option of node. Few details: 			 
	%fill=color
	%label=text of label ou label={text of label} ou label={:text of label}
	%label={position of label:text of label}
	%label={[color du label]:text of label}
	%label={[color du label]position of label:text of label}
		%text of label : characters prohibited: ; { } ,
	%draw ou draw=
	%draw=color
{Affichage}: charactères interdits: { ] ; 
	
		%\path (name node A) edge[options split by comma] (name node B);
		\path 
		() edge[] ()
		() edge[] ()
		;

%name node: to reference  to name of node set upper
%[options split by comma]:  options for edge/arc. Few details:
	%-> or <-or -: way of edge
	%"edge_label": indication on edge, for Dijkstra it's weight, for Dijkstra obligatory option 
	% edge_label : characters prohibited: ; , " \node
	%color=color: la color of edge
	\end{tikzpicture}
\end{document}

```

# exemple

```py
    x = load('Exemples/exemple_dijkstra_wiki.tex')
    A = Dijkstra(x, "node 1", "node 5")
    gen_gif(A, "versusWiki",700)
```
And for more exemple go to [github](https://github.com/Sosso8305/LaTeX-to-GIF-Python)



# Change Log 

## 0.1.1
- add Bellman-Ford algorithm
- update list of frobidden characters 
- fix problem with Ford-Fulkerson

## 0.1.0
- fix parser (now it's take - )
- change template FR to EN
- add option color for all algotithm 
- add documentation for Kruskal, Floyd-Warshall and Ford-Fulkerson

## 0.0.9
- add Kruskal algorithm
- add Floyd-Warshall algorithm
- add Ford-Fulkerson algorithm
- fix bug: the parser in funct load() take well the other_option of edge
- update template  
## 0.0.8
- change name github project 

## 0.0.7
- change documentation FR to EN

## 0.0.5
- first realese that works well


# Graphanime - create execution graph in GIF/PDF


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
		%\node (nom node) at(x,y) [options separées par virgules] {affichage} ;
		\node () at(,) [] {} ;
		\node () at(,) [] {} ;
		
%(nom node): charactères interdits: ( ) [ ] ; { } ,
%at(x,y): optionel : x et y doivent être des coordonnées viables: des nombres 
%[options séparées par virgules]:  les options du nœud. En détail certain: 			 
	%fill=couleur
	%label=texte du label ou label={texte du label} ou label={:texte du label}
	%label={position du label:texte du label}
	%label={[couleur du label]:texte du label}
	%label={[couleur du label]position du label:texte du label}
	%texte du label : charactères interdits: ; { } ,
	%draw ou draw=
	%draw=couleur{Affichage}: charactères interdits: { } [ ]; 
	
		%\path (nom node A) edge[options separées par virgules] (nom node B);
		\path 
		() edge[] ()
		() edge[] ()
		;

%nom node: fait reference à un nom de nœud défini plus haut
%[options séparées par virgules]:  les options de l’arrête/arc. En détail certain:
	%-> ou <-ou -: le sens de l’arrête
	%"edge_label": indication sur l’arrête, pour Dijkstra indique le poids, pour Dijkstra option obligatoire 
	% edge_label : charactères interdits: ; , 
	%color=couleur: la couleur de l’arrete.
	\end{tikzpicture}
\end{document}

```

# exemple

```py
    x = load('Exemples/exemple_dijkstra_wiki.tex')
    A = Dijkstra(x, "node 1", "node 5")
    gen_gif(A, "versusWiki",700)
```
And for more exemple go to [github](https://github.com/Sosso8305/GIF-Dijkstra-Python)


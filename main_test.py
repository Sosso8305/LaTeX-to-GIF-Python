# import os
# print(os.getcwd())
from graphanime import *
# from graphanime.graphanime.algorithm import Dijkstra
# from graphanime.graphanime.animation import load, gen_apng, gen_beamer, gen_gif, gen_pdf

def all_gen_Dijkstra():
    x = load('Exemples/exemple_dijkstra.tex')
    A = Dijkstra(x, "node 3", "node 5")
    gen_beamer(A,"Dijkstra_beamer")
    gen_pdf(A,"Dijkstra")
    gen_gif(A,"Dijkstra")
    gen_apng(A,"Dijkstra")

def gen_wiki():
    x = load('Exemples/exemple_dijkstra_wiki.tex')
    A = Dijkstra(x, "node 1", "node 5")
    gen_gif(A, "versusWiki",1000)
    gen_beamer(A, "versusWiki_beamer")
    gen_apng(A, "versusWiki")
   
    

def test():
    y = load("Exemples/test.tex")
    B = [y, y]
    gen_beamer(B, "test")



if __name__ == "__main__":
   
    # all_gen_Dijkstra()
    gen_wiki()
    
    
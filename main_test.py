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
    gen_gif(A, "versusWiki",700)
    gen_beamer(A, "versusWiki_beamer")
    gen_apng(A, "versusWiki")
   
def gen_floyd_warshall():
    x = load('Exemples/exemple_bellmanford.tex')
    A = Floyd_Warshall(x)
    gen_pdf(A, "warshall")
    gen_gif(A, "warshall",1000)
    gen_beamer(A, "warshall_beamer", True)
    gen_apng(A, "warshall")

def gen_floyd_warshall2():
    x = load('Exemples/exemple_floyd_warshall2.tex')
    A = Floyd_Warshall(x, bend='left')
    #gen_pdf(A, "warshall")
    gen_gif(A, "floyd_warshall",1000)
    gen_beamer(A, "warshall_beamer2", True)
    #gen_apng(A, "warshall")
    
def all_gen_FordFulkerson():
    x = load('Exemples/exemple_fordfulkerson.tex')
    A = FordFulkerson(x, x.V[0], x.V[-1])
    gen_beamer(A,"FordFulkerson_beamer")
    gen_pdf(A,"FordFulkerson")
    gen_gif(A,"FordFulkerson",700)
    gen_apng(A,"FordFulkerson",700)

def gen_Kruskal():
    x = load('Exemples/exemple_dijkstra_wiki.tex')
    anim = Kruskal(x)
    gen_gif(anim,"Kruskal")
    gen_apng(anim,"Kruskal")

    

def test():
    y = load("Exemples/exemple_fordfulkerson.tex")
    B = FordFulkerson(y)
    gen_beamer(B, "FordFulkerson")



if __name__ == "__main__":
   
    # all_gen_FordFulkerson()  
    # all_gen_Dijkstra()
    # gen_wiki()
    # gen_floyd_warshall()
    # gen_Kruskal()
    gen_floyd_warshall2()

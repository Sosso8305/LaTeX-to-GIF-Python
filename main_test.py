from graphanime import load, gen_beamer, gen_pdf, gen_gif,gen_apng
from algorithm import Dijkstra

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
    

def test():
    y = load("Exemples/test.tex")
    B = [y, y]
    gen_beamer(B, "test")



if __name__ == "__main__":
   
    gen_wiki()
    
    
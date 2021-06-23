from graphanime import load, gen_beamer
from algorithm import Dijkstra


if __name__ == "__main__":
    
    x = load('Exemples/exemple_dijkstra.tex')
    A = Dijkstra(x, "node 3", "node 5")
    gen_beamer(A,"Dijkstra")
    
from graphanime import load, gen_beamer, gen_pdf, gen_gif,gen_apng
from algorithm import Dijkstra


if __name__ == "__main__":
    
    x = load('Exemples/exemple_dijkstra.tex')
    A = Dijkstra(x, "node 3", "node 5")
    gen_beamer(A,"Dijkstra_beamer")
    gen_pdf(A,"Dijkstra")
    gen_gif(A,"Dijkstra")
    gen_apng(A,"Dijkstra")

    y = load("Exemples/test.tex")
    B = [y, y]
    gen_beamer(B, "test")
    
from heapq import heappop, heappush


INFINI = "$\infty$"

__all__ = ['Dijstra']

def Dijkstra(Graph,source,sink):
    for e in Graph.E:
        if int(Graph.weight[e]) <= 0:
            print(f"Arete {e} de poids inferieur ou egal a 0. L'algorithme de Dijkstra ne traite pas ce cas : referez-vous au Bellman-Ford")
            return [Graph]
    liste_graphes = []
    Graph_copy = Graph.copy()
    distance_from_source = 0
    priority_queue = []
    for v in Graph_copy.V:
        Graph_copy.fill[v] = "grey!50"
        Graph_copy.label[v] = INFINI
    for e in Graph_copy.E:
        Graph_copy.color[e] = "black"
    heappush(priority_queue, (0, source, [])) # Je mets dans ma file de priorités un tuple avec le noeud source et la valeur 0 (car distance de source à source = 0)
    Graph_copy.label[source] = str(0) # Le label tel que défini dans la classe Node contient la distance depuis le noeud source
    liste_graphes.append(Graph_copy.copy())
    #print("couleur, dans le graphe, du noeud ", source, " colorie : ", Graph_copy.fill[source])

    aretes_explorees = []

    i = 0
    while(priority_queue):
        for elt in priority_queue:
            print("Boucle ", i, "\tElement de la liste : ", elt)
        i += 1
        (distance_from_source, noeud, parcours) = heappop(priority_queue)
        print("Noeud sorti : ", noeud, "\tPriorite : ", distance_from_source)
        print("Parcours : ")
        for u in parcours:
            print(u)
        Graph_copy.fill[noeud] = "red"
        liste_graphes.append(Graph_copy.copy())
        if(noeud == sink):
            Graph_copy.fill[noeud] = "black"
            parcours.append(noeud)
            liste_graphes.append(Graph_copy.copy())
            break
        
        for e in Graph_copy.E:
            print("Arete : ", e)
            print("Noeud en cours : ", noeud)
            print(f"Condition e[0] = {noeud == e[0]}, Condition e[1] = {noeud == e[1]}, Condition orientation = {Graph_copy.orientation[e] == '-'}, Condition explorée = {e not in aretes_explorees}")
            if e not in aretes_explorees and ((noeud == e[0] and (Graph_copy.orientation[e] == '-' or Graph_copy.orientation[e] == '->')) or (noeud == e[1] and (Graph_copy.orientation[e] == '-' or Graph_copy.orientation[e] == '<-'))):
                print("Je suis dans le if")
                print(f"e[0] = {e[0]}, e[1] = {e[1]}, orientation = {Graph_copy.orientation[e]}")
                Graph_copy.color[e] = "green"
                liste_graphes.append(Graph_copy.copy())
                print(f"noeud = {noeud}, e[0] : {e[0]}, e[1] : {e[1]}")
                if noeud == e[0]:
                    voisin = e[1]
                else:
                    voisin = e[0]
                
                print(f"noeud = {noeud}, voisin = {voisin}")
                print(f"label du noeud : {Graph_copy.label[noeud]}, label du voisin : {Graph_copy.label[voisin]}, distance + poids : {distance_from_source + int(Graph_copy.weight[e])}")

                if (Graph_copy.label[voisin] == INFINI) or (distance_from_source + int(Graph_copy.weight[e]) < int(Graph_copy.label[voisin])): # Comme le label est un string, il faut le passer en int
                    Graph_copy.label[voisin] = str(distance_from_source + int(Graph_copy.weight[e]))
                    liste_graphes.append(Graph_copy.copy())
                    
                    heappush(priority_queue, (int(Graph_copy.label[voisin]), voisin, parcours))

                Graph_copy.color[e] = "black"
                aretes_explorees.append(e)
                
        Graph_copy.fill[noeud] = "black"
        parcours.append(noeud)
        liste_graphes.append(Graph_copy.copy())

    arete_chemin = []
    print("Parcours final : ")
    for u in parcours:
        print(u)
    for i in range(len(parcours) - 1):
        arete_chemin.append((parcours[i],parcours[i+1]))
    print (arete_chemin)
    for e in arete_chemin:
        print("e1",e[1],"e0", e[0])
        if e in Graph_copy.E:
            Graph_copy.color[e] = "blue"
        elif((e[1], e[0]) in Graph_copy.E and Graph_copy.orientation[(e[1], e[0])] == '-'):
            Graph_copy.color[(e[1], e[0])] = "blue"

    liste_graphes.append(Graph_copy.copy())
    
    return liste_graphes


def BellmanFord(Graph,source):
    
    liste_graphes = []
    Graph_copy = Graph.copy()
    distance_from_source = 0
    priority_queue = []
    for v in Graph_copy.V:
        Graph_copy.fill[v] = "grey!50"
        Graph_copy.label[v] = INFINI
    heappush(priority_queue, (0, source)) # Je mets dans ma file de priorités un tuple avec le noeud source et la valeur 0 (car distance de source à source = 0)
    Graph_copy.label[source] = str(0) # Le label tel que défini dans la classe Node contient la distance depuis le noeud source
    liste_graphes.append(Graph_copy.copy())
    Graph_copy.fill[source] = "red"
    liste_graphes.append(Graph_copy.copy())
    #print("couleur, dans le graphe, du noeud ", source, " colorie : ", Graph_copy.fill[source])

    i = 0
    while(priority_queue):
        #for elt in priority_queue:
            #print("Boucle ", i, "\tElement de la liste : ", elt)
        i += 1
        (distance_from_source, noeud) = heappop(priority_queue)
        #print("Noeud sorti : ", noeud, "\tPriorite : ", distance_from_source)
        Graph_copy.fill[noeud] = "red"
        liste_graphes.append(Graph_copy.copy())
        
        for e in Graph_copy.E:
            # print("Arete : ", e)
            # print("Noeud en cours : ", noeud)
            # print(f"Condition e[0] = {noeud == e[0]}, Condition e[1] = {noeud == e[1]}, Condition orientation = {Graph_copy.orientation[e] == '-'}")
            if (noeud == e[0]) or (noeud == e[1] and Graph_copy.orientation[e] == '-'):
                # print("Je suis dans le if")
                # print(f"e[0] = {e[0]}, e[1] = {e[1]}, orientation = {Graph_copy.orientation}")
                Graph_copy.color[e] = "green"
                liste_graphes.append(Graph_copy.copy())
                # print(f"noeud = {noeud}, e[0] : {e[0]}, e[1] : {e[1]}")
                if noeud == e[0]:
                    voisin = e[1]
                else:
                    voisin = e[0]
                
                # print(f"noeud = {noeud}, voisin = {voisin}")
                # print(f"label du noeud : {Graph_copy.label[noeud]}, label du voisin : {Graph_copy.label[voisin]}, distance + poids : {distance_from_source + int(Graph_copy.weight[e])}")

                if (Graph_copy.label[voisin] == INFINI) or (distance_from_source + int(Graph_copy.weight[e]) < int(Graph_copy.label[voisin])): # Comme le label est un string, il faut le passer en int
                    Graph_copy.label[voisin] = str(distance_from_source + int(Graph_copy.weight[e]))
                    liste_graphes.append(Graph_copy.copy())
                    heappush(priority_queue, (int(Graph_copy.label[voisin]), voisin))
                
                
        Graph_copy.fill[noeud] = "black"
        liste_graphes.append(Graph_copy.copy())
    
    return liste_graphes
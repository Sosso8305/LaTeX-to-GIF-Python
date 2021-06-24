from heapq import heappop, heappush


INFINI = "$\infty$"
DEBUG = False

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
    if DEBUG: print("couleur, dans le graphe, du noeud ", source, " colorie : ", Graph_copy.fill[source])

    noeud_explores = []
    aretes_explorees = []

    i = 0
    while(priority_queue):
        if DEBUG:
            print("=" * 50)
            for elt in priority_queue:
                print("Boucle ", i, "\tElement de la liste : ", priority_queue)
        i += 1

        (distance_from_source, noeud, parcours) = heappop(priority_queue)
        if DEBUG: print("Noeud sorti : ", noeud, "\tPriorite : ", distance_from_source, "\tParcours : ", parcours)
        if noeud not in noeud_explores:
            Graph_copy.fill[noeud] = "red"
            liste_graphes.append(Graph_copy.copy())
            if(noeud == sink):
                Graph_copy.fill[noeud] = "black"
                noeud_explores.append(noeud)
                parcours.append(noeud)
                liste_graphes.append(Graph_copy.copy())
                break
            
            for e in Graph_copy.E:
                if DEBUG:
                    print("noeuds explores : ", noeud_explores)
                    print("\t" + "*" * 50)
                    print("\tArete : ", e)
                    print("\tNoeud en cours : ", noeud)
                    print(f"\tCondition e[0] = {noeud == e[0]}, Condition e[1] = {noeud == e[1]}, Condition orientation = {Graph_copy.orientation[e] == '-'}, Condition noeud explore = {noeud not in noeud_explores}, Condition arete exploree = {e not in aretes_explorees}")
                if e not in aretes_explorees and ((noeud == e[0] and (Graph_copy.orientation[e] == '-' or Graph_copy.orientation[e] == '->')) or (noeud == e[1] and (Graph_copy.orientation[e] == '-' or Graph_copy.orientation[e] == '<-'))):
                    if DEBUG:
                        print("\t\t" + "-" * 50)
                        print("\t\tJe suis dans le if")
                        print(f"\t\te[0] = {e[0]}, e[1] = {e[1]}, orientation = {Graph_copy.orientation[e]}")
                    Graph_copy.color[e] = "green"
                    if Graph_copy.orientation[e] == '-':
                        if noeud == e[0]:
                            Graph_copy.orientation[e] = '->'
                        else:
                            Graph_copy.orientation[e] = '<-'
                    
                    liste_graphes.append(Graph_copy.copy())

                    if DEBUG: print(f"\t\tnoeud = {noeud}, e[0] : {e[0]}, e[1] : {e[1]}")

                    if noeud == e[0]:
                        voisin = e[1]
                    else:
                        voisin = e[0]
                    
                    ancien_label = Graph_copy.label[voisin]
                    Graph_copy.label[voisin] = "?"
                    liste_graphes.append(Graph_copy.copy())

                    if DEBUG:
                        print("\t\t\t" + "o" * 50)
                        print(f"\t\t\tnoeud = {noeud}, voisin = {voisin}")
                        print(f"\t\t\tlabel du noeud : {Graph_copy.label[noeud]}, label du voisin : {ancien_label}, distance + poids : {distance_from_source + int(Graph_copy.weight[e])}")

                    if (ancien_label == INFINI) or (distance_from_source + int(Graph_copy.weight[e]) < int(ancien_label)): # Comme le label est un string, il faut le passer en int
                        Graph_copy.label_color[voisin] = "green"
                        Graph_copy.label[voisin] = ancien_label + " $>$ " + str(distance_from_source) + " + " + Graph_copy.weight[e]
                        liste_graphes.append(Graph_copy.copy())
                        Graph_copy.label[voisin] = str(distance_from_source + int(Graph_copy.weight[e]))
                        chemin = parcours + [noeud]
                        heappush(priority_queue, (int(Graph_copy.label[voisin]), voisin, chemin))
                    else:
                        Graph_copy.label_color[voisin] = "red"
                        Graph_copy.label[voisin] = ancien_label + " $<$ " + str(distance_from_source) + " + " + Graph_copy.weight[e]
                        liste_graphes.append(Graph_copy.copy())
                        Graph_copy.label[voisin] = ancien_label
                        

                    Graph_copy.color[e] = "black"
                    if(Graph.orientation[e] == '-'):
                        Graph_copy.orientation[e] = '-'
                    aretes_explorees.append(e)
                    liste_graphes.append(Graph_copy.copy())
                    Graph_copy.label_color[voisin] = "black"
                    liste_graphes.append(Graph_copy.copy())
                            
            noeud_explores.append(noeud)
            Graph_copy.fill[noeud] = "black"
            parcours.append(noeud)
            liste_graphes.append(Graph_copy.copy())

    if DEBUG: print("=" * 50)
    arete_chemin = []
    if DEBUG: print("Parcours final : ", parcours)
    for i in range(len(parcours) - 1):
        arete_chemin.append((parcours[i],parcours[i+1]))
    if DEBUG: print (arete_chemin)
    for e in arete_chemin:
        if DEBUG: print("e1",e[1],"e0", e[0])
        if e in Graph_copy.E:
            Graph_copy.color[e] = "blue"
            Graph_copy.orientation[e] = '->'
        elif((e[1], e[0]) in Graph_copy.E and Graph_copy.orientation[(e[1], e[0])] == '-'):
            Graph_copy.color[(e[1], e[0])] = "blue"
            Graph_copy.orientation[(e[1], e[0])] = '<-'

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
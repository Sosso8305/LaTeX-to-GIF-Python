from heapq import heappop, heappush
from collections import defaultdict

INFINI = "$\infty$"
DEBUG = False

__all__ = ['Dijstra','BellmanFord','Kruskal']

def Dijkstra(Graph,source,sink):
    for e in Graph.E:
        if int(Graph.edge_label[e]) <= 0:
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
                        print(f"\t\t\tlabel du noeud : {Graph_copy.label[noeud]}, label du voisin : {ancien_label}, distance + poids : {distance_from_source + int(Graph_copy.edge_label[e])}")

                    if (ancien_label == INFINI) or (distance_from_source + int(Graph_copy.edge_label[e]) < int(ancien_label)): # Comme le label est un string, il faut le passer en int
                        Graph_copy.label_color[voisin] = "green"
                        Graph_copy.label[voisin] = ancien_label + " $>$ " + str(distance_from_source) + " + " + Graph_copy.edge_label[e]
                        liste_graphes.append(Graph_copy.copy())
                        Graph_copy.label[voisin] = str(distance_from_source + int(Graph_copy.edge_label[e]))
                        chemin = parcours + [noeud]
                        heappush(priority_queue, (int(Graph_copy.label[voisin]), voisin, chemin))
                    else:
                        Graph_copy.label_color[voisin] = "red"
                        Graph_copy.label[voisin] = ancien_label + " $<$ " + str(distance_from_source) + " + " + Graph_copy.edge_label[e]
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
    
    # Initialisation
    liste_graphes = []
    Graph_copy = Graph.copy()
    Graph_copy.label[source] = str(0) # Distance source à source = 0
    graph = defaultdict(dict)
    for (A,B) in Graph_copy.E :
        graph[A][B] = None
        graph[B][A] = None
    for i in graph :
        for j in graph[i]:
            for e in Graph_copy.E :
                if (i,j) == e:
                    graph[i][j] = Graph_copy.edge_label[e]
                elif (j,i) == e:
                    graph[i][j] = Graph_copy.edge_label[e]

    # Initialisation graphique
    for v in Graph_copy.V:
        Graph_copy.fill[v] = "grey!50"
        Graph_copy.label[v] = INFINI
    for e in Graph_copy.E:
        Graph_copy.color[e] = "black"
    liste_graphes.append(Graph_copy.copy())
    if DEBUG: print("couleur, dans le graphe, du noeud ", source, " colorie : ", Graph_copy.fill[source])

    # Début (mathématique)
    distances = {}
    predecesseurs = {}
    for noeud in graph :
        distances[noeud] = 'infini'
        predecesseurs[noeud] = None
    distances[source]= 0

    # Corps
    for k in range(len(graph) - 1):
        for i in graph :
            for j in graph[i]:
                if distances[j] > distances[i] + graph[i][j]:
                    distances[j]  = distances[i] + graph[i][j]
                    predecesseurs[j] = i
    
    for i in graph :
        for j in graph[i]:
            if distances[j] <= distances[i] + graph[i][j]:
                return "Donne un GRAPH QUI PEUT MARCHER!!!!!\n"
    
    return distances, predecesseurs



def cycleUtils(current_node,visited,parent,graph):
    
    visited[current_node]=True
  
    for node in graph[current_node]:
        
        if not visited[node]:
            if cycleUtils(node, visited, current_node, graph):
                return True
        
        elif parent != node:
            return True
          
    return False
            
    

def is_cycle(E):
    graph = {}
    visited = {}

    for edge in E:
        node1, node2= edge
        for x, y in [(node1, node2), (node2, node1)]:
            if x in graph:
                graph[x].append(y)
            else:
                graph[x] = [y]

        visited[node1]=False
        visited[node2]=False
    

    for node in visited:
    
        if not visited[node]:
            if cycleUtils(node,visited,"-1",graph):
                return True

     

    return False



def Kruskal(Graph):
    graph_list=[]
    Graph=Graph.copy()
    #may be set color of graph 
    graph_list.append(Graph.copy())


    spanning_tree=[]
    weight_spanning_tree=0
    edge_list=[]
    for e in Graph.E:
        heappush(edge_list,(int(Graph.edge_label[e]),e))


    while edge_list:
        (weight,edge) = heappop(edge_list)

        Graph.color[edge]="blue"
        graph_list.append(Graph.copy())
        graph_list.append(Graph.copy())

        spanning_tree.append(edge)

        if is_cycle(spanning_tree):
            spanning_tree.remove(edge)
            Graph.color[edge]="grey!10"
            graph_list.append(Graph.copy())
        else:
            Graph.color[edge]="green"
            graph_list.append(Graph.copy())
            weight_spanning_tree += weight

    

    return graph_list



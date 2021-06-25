from heapq import heappop, heappush
from collections import defaultdict

INFINI = "$\infty$"
DEBUG = False

__all__ = ['Dijstra','BellmanFord', 'FordFulkerson','Kruskal', 'Floyd_Warshall']

# #########################################################
# ############# Dijkstra ALGORYTHM #############
# #########################################################

def Dijkstra(Graph,source,sink):
    for e in Graph.E:
        if int(Graph.edge_label[e]) <= 0:
            print(f"Arete {e} de poids inferieur ou egal a 0. L'algorithme de Dijkstra ne traite pas ce cas : referez-vous au Bellman-Ford")
            return [Graph]

    liste_graphes = [] # Liste contenant tous les états du graphe
    Graph_copy = Graph.copy() # On travaille sur une copie
    distance_from_source = 0 # Distance du noeud d'origine au noeud actuellement étudié
    priority_queue = [] # Liste des noeuds à traiter. Celui avec la distance au noeud source la plus faible sort en premier
    
    for v in Graph_copy.V:
        Graph_copy.fill[v] = "grey!50"
        Graph_copy.label[v] = INFINI
    for e in Graph_copy.E:
        Graph_copy.color[e] = "black"
    Graph_copy.contour_color[source] = "red!50"
    Graph_copy.contour_color[sink] = "red!50"

    heappush(priority_queue, (0, source, [])) # Je mets dans ma file de priorités un tuple avec le noeud source, la valeur 0 (car distance de source à source = 0) et une liste vide (le chemin du noeud source au noeud source est une liste vide)
    Graph_copy.label[source] = str(0) # Le label tel que défini dans la classe Node contient la distance depuis le noeud source
    liste_graphes.append(Graph_copy.copy())
    if DEBUG: print("couleur, dans le graphe, du noeud ", source, " colorie : ", Graph_copy.fill[source])

    # On ne traite pas les noeuds ni les arêtes déjà explorés
    noeud_explores = []
    aretes_explorees = []

    i = 0
    while(priority_queue): # Tant que la file n'est pas vide
        if DEBUG:
            print("=" * 50)
            for elt in priority_queue:
                print("Boucle ", i, "\tElement de la liste : ", priority_queue)
        i += 1

        (distance_from_source, noeud, parcours) = heappop(priority_queue) # On récupère le noeud à traiter (celui qui est le plus proche de la source), le parcours pour y arriver, et la longueur du trajet
        if DEBUG: print("Noeud sorti : ", noeud, "\tPriorite : ", distance_from_source, "\tParcours : ", parcours)
        if noeud not in noeud_explores:
            Graph_copy.fill[noeud] = "red" # On colore le noeud actuellement étudié
            liste_graphes.append(Graph_copy.copy())
            if(noeud == sink): # Si c'est le noeud objectif, on arrête l'exécution de l'algorithme
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
                    # Cette condition permet de s'assurer que :
                    #     1/ Le noeud n'a pas déjà été étudié
                    #     2/ Le noeud étudié est dans l'arête nommée 'e' :
                    #         a/ Soit on a une arête x--y, et noeud étudié = x ou y
                    #         b/ Soit on a une arête x->y, et noeud étudié = x
                    #         c/ Soit on a une arête x<-y, et noeud étudié = y
                    if DEBUG:
                        print("\t\t" + "-" * 50)
                        print("\t\tJe suis dans le if")
                        print(f"\t\te[0] = {e[0]}, e[1] = {e[1]}, orientation = {Graph_copy.orientation[e]}")
                    
                    # On colore l'arête actuellement étudiée en vert. 
                    # Si l'arête n'est pas orientée, on l'oriente pour rendre la lecture plus facile
                    Graph_copy.color[e] = "green"
                    if Graph_copy.orientation[e] == '-':
                        if noeud == e[0]:
                            Graph_copy.orientation[e] = '->'
                        else:
                            Graph_copy.orientation[e] = '<-'
                    liste_graphes.append(Graph_copy.copy())

                    if DEBUG: print(f"\t\tnoeud = {noeud}, e[0] : {e[0]}, e[1] : {e[1]}")

                    # On définit, pour une arête donnée, le voisin du noeud actuellement étudié
                    if noeud == e[0]:
                        voisin = e[1]
                    else:
                        voisin = e[0]
                    
                    # On remplace le label du noeud voisin par '?' pour montrer que c'est sur lui que porte l'étude
                    ancien_label = Graph_copy.label[voisin]
                    Graph_copy.label[voisin] = "?"
                    liste_graphes.append(Graph_copy.copy())

                    if DEBUG:
                        print("\t\t\t" + "o" * 50)
                        print(f"\t\t\tnoeud = {noeud}, voisin = {voisin}")
                        print(f"\t\t\tlabel du noeud : {Graph_copy.label[noeud]}, label du voisin : {ancien_label}, distance + poids : {distance_from_source + int(Graph_copy.edge_label[e])}")

                    if (ancien_label == INFINI) or (distance_from_source + int(Graph_copy.edge_label[e]) < int(ancien_label)): # Comme le label est un string, il faut le passer en int
                        # Si on trouve un chemin améliorant, on montre que ce chemin est plus court que celui qui était jusque là retenu
                        # On colore le label en vert, et on y inscrit la nouvelle valeur
                        # De plus, on ajoute ce noeud dans la file, avec le parcours nécessaire jusque là
                        Graph_copy.label_color[voisin] = "green"
                        Graph_copy.label[voisin] = ancien_label + " $>$ " + str(distance_from_source) + " + " + Graph_copy.edge_label[e]
                        liste_graphes.append(Graph_copy.copy())
                        Graph_copy.label[voisin] = str(distance_from_source + int(Graph_copy.edge_label[e]))
                        chemin = parcours + [noeud]
                        heappush(priority_queue, (int(Graph_copy.label[voisin]), voisin, chemin))
                    else:
                        # Sinon, on  colore le label en rouge, et on garde l'ancienne valeur
                        Graph_copy.label_color[voisin] = "red"
                        Graph_copy.label[voisin] = ancien_label + " $<$ " + str(distance_from_source) + " + " + Graph_copy.edge_label[e]
                        liste_graphes.append(Graph_copy.copy())
                        Graph_copy.label[voisin] = ancien_label
                        

                    # On réinitialise l'arête à son état avant traitement
                    Graph_copy.color[e] = "black"
                    if(Graph.orientation[e] == '-'):
                        Graph_copy.orientation[e] = '-'
                    aretes_explorees.append(e)
                    liste_graphes.append(Graph_copy.copy())
                    Graph_copy.label_color[voisin] = "black"
                    liste_graphes.append(Graph_copy.copy())
                            
            # On ajoute le noeud à la liste des noeuds déjà étudiés, et on le colore en noir pour montrer qu'on a fini
            noeud_explores.append(noeud)
            Graph_copy.fill[noeud] = "black"
            parcours.append(noeud)
            liste_graphes.append(Graph_copy.copy())

    if DEBUG: 
        print("=" * 50)
        print("Parcours final : ", parcours)
    
    # Dans la liste 'parcours', on a noté les noeuds par lesquels il fallait passer.
    # Maintenant, on transforme cette suite de noeuds en suite d'arêtes
    # On colore en bleu les arêtes du plus court chemin trouvé grâce à l'algorithme, et on les oriente
    arete_chemin = []
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


# #########################################################
# ######### METHODS FOR FORD-FULKERSON ALGORITHM ##########
# #########################################################
class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

def getSuccessors(Graph, source):
    successors = []
    for e in Graph.E:
        if (source == e[0] and Graph.orientation[e] == '->'):
            successors.append(e[1])
        if (source == e[1] and Graph.orientation[e] == '<-'):
            successors.append(e[0])
    
    return successors

def getPredecessors(Graph, source):
    predecessors = []
    for e in Graph.E:
        if (source == e[0] and Graph.orientation[e] == '<-'):
            predecessors.append(e[1])
        if (source == e[1] and Graph.orientation[e] == '->'):
            predecessors.append(e[0])
    
    return predecessors

def depthFirstSearch(Graph, source, target, flow, capacity):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """

    border = Stack() 
    path = [] 
    border.push((source, path))
    explored = []

    if source == target: 
        return path
    while(True):
        if(border.isEmpty()):
            print('Empty border')
            return None

        node, path = border.pop()
        explored.append(node)
        if node == target:
            path.append(node)
            return path

        successors = getSuccessors(Graph, node)
        predecessors = getPredecessors(Graph, node)
        route = []
        if successors:
            for i in range(len(successors)):
                child_node = successors[-i-1]
                if child_node not in explored and capacity[(node, child_node)] > flow[(node, child_node)]:
                    route = path + [node]
                    border.push((child_node, route)) 
        elif predecessors:
            for i in range(len(predecessors)):
                father_node = predecessors[-i-1]
                if father_node not in explored and flow[(father_node, node)] > 0:
                    route = path + [node]
                    border.push((father_node, route)) 

        if route == []:
            return None




def FordFulkerson(Graph):
    flow = {arete : 0 for arete in Graph.E}
    capacity = {arete : int(Graph.edge_label[arete]) for arete in Graph.E}
    graph_list = []

    Graph_copy = Graph.copy()
    for v in Graph_copy.V:
        Graph_copy.fill[v] = "grey!50"
    for e in Graph_copy.E:
        Graph_copy.color[e] = "black"
    Graph_copy.contour_color[Graph_copy.V[0]] = "red!50"
    Graph_copy.contour_color[Graph_copy.V[-1]] = "red!50"
    graph_list.append(Graph_copy.copy())

    better_way_nodes = depthFirstSearch(Graph_copy, Graph_copy.V[0], Graph_copy.V[-1], flow, capacity)
    while(better_way_nodes):
        if DEBUG:
            print("=" * 50)
            print("Chemin trouvé : ", better_way_nodes)
            print("Flots avant execution : ", flow)
        better_way_edges = []
        for i in range(len(better_way_nodes) - 1):
            better_way_edges.append((better_way_nodes[i],better_way_nodes[i+1]))
        
        edges_to_increase = []
        edges_to_lower = []
        for edge in better_way_edges:
            if edge in Graph_copy.E:
                edges_to_increase.append(edge)
            elif (edge[1], edge[0]) in Graph_copy.E:
                edges_to_lower.append((edge[1], edge[0]))

        for e in edges_to_increase + edges_to_lower:
            Graph_copy.color[e] = "green"
        graph_list.append(Graph_copy.copy())            
        
        flow_of_way = min([capacity[e] - flow[e] for e in edges_to_increase] + [flow[e] for e in edges_to_lower])

        for e in edges_to_increase:
            flow[e] += flow_of_way
        for e in edges_to_lower:
            flow[e] -= flow_of_way

        for e in Graph_copy.E:
            Graph_copy.edge_label[e] = str(capacity[e] - flow[e])
        
        graph_list.append(Graph_copy.copy())

        for e in Graph_copy.E:
            if(capacity[e] - flow[e] == 0):
                Graph_copy.edge_options[e] = "dashed"
                Graph_copy.color[e] = "red!25"
            else:
                Graph_copy.color[e] = "black"

        graph_list.append(Graph_copy.copy())

        if DEBUG:
            print("Flots apres execution : ", flow)
            print("Capacites : ", capacity)

        better_way_nodes = depthFirstSearch(Graph_copy, Graph_copy.V[0], Graph_copy.V[-1], flow, capacity)


    graph_list[0].preambule += "\n\\usepackage{ulem}"
    return graph_list
    

# #########################################################
# ############# METHODS FOR KRUSKAL ALGORITHM #############
# #########################################################
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



def Kruskal(Graph,display_weight=False,color_current_edge="blue",color_good_edge="green",color_wrong_edge="grey!10"):
    """It's execute Kruskal's algorithm 

    Args:
        Graph (Graph): class Graph  
        display_weight (bool, optional): it's a weight of spanning tree. Defaults to False.
        color_current_edge (str, optional): edge who is process. Defaults to "blue".
        color_good_edge (str, optional): edge who is add to spanning tree. Defaults to "green".
        color_wrong_edge (str, optional): edge who create a cycle in spanning tree. Defaults to "grey!10".

    Returns:
        [list of Graph]: it's use for genereted a file with Back-end
    """
    graph_list=[]
    Graph=Graph.copy()
    graph_list.append(Graph.copy())


    spanning_tree=[]
    weight_spanning_tree=0
    edge_list=[]
    for e in Graph.E:
        heappush(edge_list,(int(Graph.edge_label[e]),e))


    while edge_list:
        (weight,edge) = heappop(edge_list)

        Graph.color[edge]=color_current_edge
        graph_list.append(Graph.copy())
        graph_list.append(Graph.copy())

        spanning_tree.append(edge)

        if is_cycle(spanning_tree):
            spanning_tree.remove(edge)
            Graph.color[edge]=color_wrong_edge
            graph_list.append(Graph.copy())
        else:
            Graph.color[edge]=color_good_edge
            graph_list.append(Graph.copy())
            weight_spanning_tree += weight


    if display_weight: print("The weight of spanning tree --> ", weight_spanning_tree)

    return graph_list

# #########################################################
# ############# FLOYD MARSHALL ALGORYTHM #############
# #########################################################

# L'algorythme marche différemment en cas de graph orienté et non orienté, si un graph est orienté alors attention : en cas d'arrete notre algorythme les transformera en double arc, mais pas très joliment
def Floyd_Warshall(Graph):
    oriented = False
    for e in Graph.E:
        if Graph.orientation[e]!='-':
            oriented = True
            break
    Graph=Graph.copy()
    # On transforme d'abord le graph en graph orienté dans un seul sens
    if oriented:
        for e in Graph.E:
            if Graph.orientation[e]=='-':
                Graph.orientation[e]='->'
                Graph.E.append((e[1],e[0]))
                Graph.orientation[(e[1],e[0])]='->'
                Graph.edge_label[(e[1],e[0])]=Graph.edge_label[e]
                Graph.color[(e[1],e[0])]=Graph.color[e]
                Graph.edge_options[(e[1],e[0])]=Graph.edge_options[e]
            if Graph.orientation[e]=='<-':
                if (e[1],e[0]) in Graph.E:
                    Graph.orientation[e]='->'
                    Graph.orientation[(e[1],e[0])]='->'
                    tmp_edge_label=Graph.edge_label[(e[1],e[0])]
                    tmp_color= Graph.color[(e[1],e[0])]
                    tmp_options=Graph.edge_options[(e[1],e[0])]
                    Graph.edge_label[(e[1],e[0])]=Graph.edge_label.pop(e)
                    Graph.color[(e[1],e[0])]=Graph.color.pop(e)
                    Graph.edge_options[(e[1],e[0])]=Graph.edge_options.pop(e)
                    Graph.edge_label[e]=tmp_edge_label
                    Graph.color[e]=tmp_color
                    Graph.edge_options[e]=tmp_options
                else:
                    Graph.E.remove(e)
                    Graph.E.append((e[1],e[0]))
                    Graph.orientation[(e[1],e[0])]='->'
                    Graph.edge_label[(e[1],e[0])]=Graph.edge_label.pop(e)
                    Graph.color[(e[1],e[0])]=Graph.color.pop(e)
                    Graph.edge_options[(e[1],e[0])]=Graph.edge_options.pop(e)

    # Application de l'algorythme
    liste_graphes=[Graph.copy()]
    for k in Graph.V:
        for i in Graph.V:
            for j in Graph.V:
                path = (i,j)
                shortcut1=(i,k)
                shortcut2=(k,j)
                if i == j:
                    continue
                if oriented:
                    if shortcut1 not in Graph.E or shortcut2 not in Graph.E:
                        continue
                    if path not in Graph.E:
                        Graph.E.append(path)
                        Graph.orientation[path]='->'
                    #dist=str(int(Graph.edge_label[shortcut1])+int(Graph.edge_label[shortcut2]))
                else:
                    if shortcut1 not in Graph.E:
                        shortcut1=(k,i)
                    if shortcut2 not in Graph.E:
                        shortcut2=(j,k)
                    if shortcut1 not in Graph.E or shortcut2 not in Graph.E:
                        continue
                    if (i,j) not in Graph.E and (j,i) in Graph.E:
                        continue
                    if path not in Graph.E:
                        Graph.E.append(path)
                        Graph.orientation[path]='-'
                    #dist=str(int(Graph.edge_label[((i,k) if (i,k) in Graph.E else (k,i))])+int(Graph.edge_label[((k,j) if (k,j) in Graph.E else (j,k))]))
                dist=str(int(Graph.edge_label[shortcut1])+int(Graph.edge_label[shortcut2]))
                tmp_color1=Graph.color[shortcut1]
                tmp_color2=Graph.color[shortcut2]
                tmp_contour=Graph.contour_color[k]
                Graph.color[shortcut1]='red'
                Graph.color[shortcut2]='red'
                Graph.contour_color[k]='red'
                modified =False
                if path not in Graph.edge_label.keys() or int(Graph.edge_label[path]) > int(dist):
                    Graph.edge_label[path] = dist
                    Graph.color[path]='green'
                    modified = True
                liste_graphes.append(Graph.copy())
                Graph.color[shortcut1]=tmp_color1
                Graph.color[shortcut2]=tmp_color2
                Graph.contour_color[k]=tmp_contour
                if not tmp_contour:
                    Graph.contour_color.pop(k)
                if modified: Graph.color[path]='pink'
    liste_graphes.append(Graph)
    return liste_graphes

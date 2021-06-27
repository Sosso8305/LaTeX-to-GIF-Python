from heapq import heappop, heappush
from collections import defaultdict

INFINITE = "$\infty$"
DEBUG = False

__all__ = ['Dijstra','BellmanFord', 'FordFulkerson','Kruskal', 'Floyd_Warshall']

# #########################################################
# ############# Dijkstra ALGORYTHM #############
# #########################################################

def Dijkstra(Graph,source,sink, not_explored_node_color="grey!50", default_edge_color="black", begin_color="red!50", end_color="red!50", current_node_color="red", current_edge_color="green", default_label_color="black", better_way_label_color="green", no_better_way_label_color="red", explored_node_color="black", final_path_color="blue"):
    """
    Application of the Ford-Fulkerson algorithm, to find the maximum flow from the source node to the target.
    Actually, this specific function colors and changes labels of the graph to illustrate the algorithm.
    It returns a list containing the different states of the graph.

    Args:
        Graph (class Graph): The graph on which the algorithm will be applied.
        source (String): Name of the source node.
        sink (String): Name of the well node.
        not_explored_node_color (str, optional): Color for nodes that have not already been explored. Defaults to "grey!50".
        default_edge_color (str, optional): Default color for edges, when they are not explored. Defaults to "black".
        begin_border_color (str, optional): Color of the border surrounding the initial node. Defaults to "red!50".
        end_border_color (str, optional): Color of the border surrounding the final node. Defaults to "red!50".
        current_edge_color (str, optional): Color of the edge that is currently explored. Defaults to "green".
        current_node_color (str, optional): Color of the node that is currently explored. Defaults to "red".
        default_label_color (str, optional): Default color for node labels. Defaults to "black".
        better_way_label_color (str, optional): Color for node labels when the algorithm has found an improving way. Defaults to "green".
        no_better_way_label_color (str, optional): Color for node labels when the algorithm has not found any improving way. Defaults to "red".
        explored_node_color (str, optional): Color of the nodes that have been explored. This color immediatly succeeds to 'current_edge_color'. Defaults to "black".
        final_path_color (str, optional): Color of the edges in the final path from source to sink, computed by the algorithm. Defaults to "blue".

    Returns:
        [List]: List containing the differents states of the graph, like "frames". Each time a change is made, a copy of the graph is saved in the list.
    """
    for e in Graph.E:
        if int(Graph.edge_label[e]) <= 0:
            print(f"Arete {e} de poids inferieur ou egal a 0. L'algorithme de Dijkstra ne traite pas ce cas : referez-vous au Bellman-Ford")
            return [Graph]

    graph_list = [] # List containing the differents states of the graph
    Graph_copy = Graph.copy() # The algorithm works on a copy of the graph
    distance_from_source = 0 # Distance between source node and sink node
    priority_queue = [] # LIFO list containing the nodes that must be explored. The one with the smallest distance to the source node goes out first
    
    # Default syntax values
    for v in Graph_copy.V:
        Graph_copy.fill[v] = not_explored_node_color
        Graph_copy.label[v] = INFINITE
    for e in Graph_copy.E:
        Graph_copy.color[e] = default_edge_color
    Graph_copy.contour_color[source] = begin_color
    Graph_copy.contour_color[sink] = end_color

    heappush(priority_queue, (0, source, [])) # In the list, we push a tuple. The first one contains 0 (= distance from source to source), the source node and an empty list (the path from source to source)
    Graph_copy.label[source] = str(0) # The label of the node (which is a string) contains, in this algorithm, the distance from the source node. Its value is 0 for the source node
    graph_list.append(Graph_copy.copy())
    if DEBUG: print("Node ", source, ": color: ", Graph_copy.fill[source])

    # The algorithm does not explore nodes nor edges that have already been explored
    explored_nodes = []
    explored_edges = []

    i = 0
    while(priority_queue): # While there is a node to explore
        if DEBUG:
            print("=" * 50)
            print("Loop ", i, "\tElements in priority queue: ", priority_queue)
        i += 1

        (distance_from_source, node, path) = heappop(priority_queue) # Sorts the node to be treated (the one that is closest to the source), the path from the source to the node, and the distance from the source
        if DEBUG: print("Sorted node: ", node, "\Priority: ", distance_from_source, "\tParcours : ", path)
        if node not in explored_nodes:
            Graph_copy.fill[node] = current_node_color # Colors the currently treated node
            graph_list.append(Graph_copy.copy())
            if(node == sink): # If the treated node is the goal defined by the user, the algorithm stops its execution
                Graph_copy.fill[node] = explored_node_color # The goal node is colored as an explored node
                explored_nodes.append(node)
                path.append(node)
                graph_list.append(Graph_copy.copy())
                break
            
            for e in Graph_copy.E:
                if DEBUG:
                    print("Explored nodes: ", explored_nodes)
                    print("\t" + "*" * 50)
                    print("\tEdges : ", e)
                    print("\tCurrent nodes: ", node)
                    print(f"\tCondition e[0] = {node == e[0]}, Condition e[1] = {node == e[1]}, Condition orientation = {Graph_copy.orientation[e] == '-'}, Condition explored node = {node not in explored_nodes}, Condition explored edge  = {e not in explored_edges}")
                if e not in explored_edges and ((node == e[0] and (Graph_copy.orientation[e] == '-' or Graph_copy.orientation[e] == '->')) or (node == e[1] and (Graph_copy.orientation[e] == '-' or Graph_copy.orientation[e] == '<-'))):
                    # This condition asserts that:
                    #     1/ The node has not already been treated
                    #     2/ The currently explored node is in the graph:
                    #         a/ Either the edge is x--y, and explored node = x or y
                    #         b/ Or the edge is x->y, and explored node = x
                    #         c/ Or the edge is x<-y, and explored node = y
                    if DEBUG:
                        print("\t\t" + "-" * 50)
                        print(f"\t\te[0] = {e[0]}, e[1] = {e[1]}, orientation = {Graph_copy.orientation[e]}")
                    
                    # The currently treated edge is colored 
                    # If the edge is not already oriented, the algorithm orientates it to make the animation easier to read
                    Graph_copy.color[e] = current_edge_color
                    if Graph_copy.orientation[e] == '-':
                        if node == e[0]:
                            Graph_copy.orientation[e] = '->'
                        else:
                            Graph_copy.orientation[e] = '<-'
                    graph_list.append(Graph_copy.copy())

                    if DEBUG: print(f"\t\tnode = {node}, e[0] : {e[0]}, e[1] : {e[1]}")

                    # For a given edge, we must define the neighbour of the currently explored node
                    if node == e[0]:
                        neighbour = e[1]
                    else:
                        neighbour = e[0]
                    
                    # The treated neighbour's label is changed: now it contains '?', to emphasize that the algorithm determines if the current path (from the source to this neighbour) is better than the previous one
                    old_label = Graph_copy.label[neighbour]
                    Graph_copy.label[neighbour] = "?"
                    graph_list.append(Graph_copy.copy())

                    if DEBUG:
                        print("\t\t\t" + "o" * 50)
                        print(f"\t\t\tnode = {node}, neighbour = {neighbour}")
                        print(f"\t\t\tnode label: {Graph_copy.label[node]}, neighbour's label: {old_label}, distance + weight: {distance_from_source + int(Graph_copy.edge_label[e])}")

                    if (old_label == INFINITE) or (distance_from_source + int(Graph_copy.edge_label[e]) < int(old_label)): # As label is a string, it must be converted to int
                        # If an improving path is found, it is written in the label that this path is shorter than the one previously chosen
                        # We colour the label with better_way_label_color, and write the new value
                        # In addition, we add this node to the queue, along with the path required so far
                        Graph_copy.label_color[neighbour] = better_way_label_color
                        Graph_copy.label[neighbour] = old_label + " $>$ " + str(distance_from_source) + " + " + Graph_copy.edge_label[e]
                        graph_list.append(Graph_copy.copy())
                        Graph_copy.label[neighbour] = str(distance_from_source + int(Graph_copy.edge_label[e]))
                        chemin = path + [node]
                        heappush(priority_queue, (int(Graph_copy.label[neighbour]), neighbour, chemin))
                    else:
                        # Else, we colour the label with better_way_label_color, and keep the old value
                        Graph_copy.label_color[neighbour] = no_better_way_label_color
                        Graph_copy.label[neighbour] = old_label + " $<$ " + str(distance_from_source) + " + " + Graph_copy.edge_label[e]
                        graph_list.append(Graph_copy.copy())
                        Graph_copy.label[neighbour] = old_label
                        

                    # The edge is reset to its state before treatment
                    Graph_copy.color[e] = default_edge_color
                    if(Graph.orientation[e] == '-'):
                        Graph_copy.orientation[e] = '-'
                    explored_edges.append(e)
                    graph_list.append(Graph_copy.copy())
                    Graph_copy.label_color[neighbour] = default_label_color
                    graph_list.append(Graph_copy.copy())
                            
            # The node is added to the lists of explored nodes and is coloured with explored_node_color
            explored_nodes.append(node)
            Graph_copy.fill[node] = explored_node_color
            path.append(node)
            graph_list.append(Graph_copy.copy())

    if DEBUG: 
        print("=" * 50)
        print("Parcours final : ", path)
    
    # In the 'path' list, we have noted the nodes through which we must pass.
    # Now, we transform this sequence of nodes into a sequence of edges
    # We colour with final_path_color the edges of the shortest path found thanks to the algorithm, and we orient them
    edges_of_path = []
    for i in range(len(path) - 1):
        edges_of_path.append((path[i],path[i+1]))
    if DEBUG: print (edges_of_path)
    for e in edges_of_path:
        if DEBUG: print("e1",e[1],"e0", e[0])
        if e in Graph_copy.E:
            Graph_copy.color[e] = final_path_color
            Graph_copy.orientation[e] = '->'
        elif((e[1], e[0]) in Graph_copy.E and Graph_copy.orientation[(e[1], e[0])] == '-'):
            Graph_copy.color[(e[1], e[0])] = final_path_color
            Graph_copy.orientation[(e[1], e[0])] = '<-'
    graph_list.append(Graph_copy.copy())
    
    return graph_list


def BellmanFord(Graph,source):
    
    # Initialisation
    liste_graphes = []
    Graph_copy = Graph.copy()
    Graph_copy.label[source] = str(0) # Distance source à source = 0
    graph = defaultdict(dict)

    # Initialisation graphique
    for v in Graph_copy.V:
        Graph_copy.fill[v] = "grey!50"
        Graph_copy.label[v] = INFINITE
    for e in Graph_copy.E:
        Graph_copy.color[e] = "black"
    Graph_copy.contour_color[source] = "red!50"

    # Construction dictionnaire voisin avec poids => {'noeud':{'voisin' : poids, ...}, ... }
    for e in Graph_copy.E :
        if Graph_copy.orientation[e] == '-' :
            graph[e[0]][e[1]] = None
            graph[e[1]][e[0]] = None
        elif Graph_copy.orientation[e] == '->':
            graph[e[0]][e[1]] = None
            if e[1] not in graph.keys():
                graph[e[1]] = {}
        elif Graph_copy.orientation[e] == '<-' :
            graph[e[1]][e[0]] = None
            if e[0] not in graph.keys():
                graph[e[0]] = {}
    for i in graph :
        for j in graph[i]:
            for e in Graph_copy.E :
                if Graph_copy.orientation[e] == '-':
                    if e == (i,j):
                        graph[i][j] = int(Graph_copy.edge_label[e])
                    elif e == (j,i):
                        graph[i][j] = int(Graph_copy.edge_label[e])
                elif Graph_copy.orientation[e] == '->': 
                    if e == (i,j):
                        graph[i][j] = int(Graph_copy.edge_label[e])
                elif Graph_copy.orientation[e] == '<-': 
                    if (e[1],e[0]) == (i,j):
                        graph[i][j] = int(Graph_copy.edge_label[e]) 

    if DEBUG : print(graph)

    # Début 
    negative_cycle = False
    distances = {}
    predecesseurs = {}
    for noeud in graph :
        distances[noeud] = INFINITE
        predecesseurs[noeud] = None
    distances[source]= 0
    Graph_copy.label[source] = 0
    if DEBUG : print(distances)
    liste_graphes.append(Graph_copy.copy())

    # Corps
    ancien_j = None
    ancien_e = None
    for k in range(len(graph) - 1):
        for i in graph : 
            for j in graph[i]:
                if (distances[i]!=INFINITE) and (distances[j]==INFINITE or (distances[j] > distances[i] + graph[i][j])):
                    if ancien_j != None and ancien_e != None:
                        Graph_copy.label_color[ancien_j] = "black"
                        Graph_copy.fill[ancien_j] = "grey!50"
                        Graph_copy.color[ancien_e] = "black"
                        liste_graphes.append(Graph_copy.copy())
                    Graph_copy.label_color[j] = "red"
                    Graph_copy.label[j] = str(distances[j]) + " $>$ " + str(distances[i]) + " + " + str(graph[i][j])
                    for e in Graph_copy.E :
                        if Graph_copy.orientation[e] == '-':
                            if e == (i,j):
                                Graph_copy.color[e] = "red"
                                ancien_e = e
                            elif e == (j,i):
                                Graph_copy.color[e] = "red"
                                ancien_e = e
                        elif Graph_copy.orientation[e] == '->': 
                            if e == (i,j):
                               Graph_copy.color[e] = "red"
                               ancien_e = e
                        elif Graph_copy.orientation[e] == '<-': 
                            if e == (j,i):
                               Graph_copy.color[e] = "red"
                               ancien_e = e
                    liste_graphes.append(Graph_copy.copy())
                    distances[j] = distances[i] + graph[i][j]
                    Graph_copy.label[j] = distances[j]
                    Graph_copy.fill[j] = "red"
                    liste_graphes.append(Graph_copy.copy())
                    ancien_j = j
                    predecesseurs[j] = i
    Graph_copy.label_color[ancien_j] = "black"
    Graph_copy.fill[ancien_j] = "grey!50"
    Graph_copy.color[ancien_e] = "black"
    liste_graphes.append(Graph_copy.copy())
          
    if DEBUG :
        print(distances)
        print(predecesseurs)
    
    # Detecteur de circuit absorbant
    for i in graph :
        for j in graph[i]:
            if (j != source)and (distances[i]!=INFINITE) and (distances[j] > distances[i] + graph[i][j]):
                negative_cycle = True
                vertex = j

    # Affichage circuit absorbant
    if negative_cycle :
        #vertex may not be in the cycle
        for i in range(len(Graph_copy.V)):  
            vertex = predecesseurs[vertex]
        #vertex is in the cycle

        cycle = []
        vertex_of_cycle = vertex
        while True :
            cycle.append(vertex_of_cycle)
            if (vertex_of_cycle == vertex) and (len(cycle)>1):
                break
            vertex_of_cycle = predecesseurs[vertex_of_cycle]
        # Cycle is reversed
        cycle.reverse()

        # Nodes of the negative cycle
        for nodes in cycle:
            Graph_copy.fill[nodes] = "green"
            Graph_copy.label[nodes] = "- cycle"

        # Edges of the negative cycle
        chemin = []
        for i in range(len(cycle)-1):
            chemin.append((cycle[i], cycle[i+1]))
        for edge in chemin:
            for e in Graph_copy.E :
                if Graph_copy.orientation[e] == '->': 
                    if e == edge:
                        Graph_copy.color[e] = "green"
                elif Graph_copy.orientation[e] == '<-': 
                    if e == (edge[1],edge[0]):
                        Graph_copy.color[e] = "green"
        liste_graphes.append(Graph_copy.copy()) 


    # Affichage plus courts chemins
    if not negative_cycle :
        chemin = [(k,v) for k,v in predecesseurs.items()]
        chemin.remove((source, None))
        for edge in chemin:
            for e in Graph_copy.E :
                if Graph_copy.orientation[e] == '-':
                    if e == edge:
                        Graph_copy.color[e] = "green"
                        Graph_copy.orientation[e]='<-'
                    elif e == (edge[1],edge[0]):
                        Graph_copy.color[e] = "green"
                        Graph_copy.orientation[e]='->'
                elif Graph_copy.orientation[e] == '<-': 
                    if e == edge:
                        Graph_copy.color[e] = "green"
                elif Graph_copy.orientation[e] == '->': 
                    if e == (edge[1],edge[0]):
                        Graph_copy.color[e] = "green"
        liste_graphes.append(Graph_copy.copy()) 

    #return distances
    return liste_graphes


# #########################################################
# ######### METHODS FOR FORD-FULKERSON ALGORITHM ##########
# #########################################################
class Stack:
    """
    A container with a last-in-first-out (LIFO) queuing policy.
    """
    def __init__(self):
        self.list = []

    def push(self,item):
        """
        Push 'item' onto the stack

        Args:
            item ([Node]): node that will be pushed on the stack
        """
        self.list.append(item)

    def pop(self):
        """
        Pop the most recently pushed item from the stack

        Returns:
            [Node]: The last item (in this case, the last node) that has been pushed on the stack
        """
        return self.list.pop()

    def isEmpty(self):
        """
        Returns true if the stack is empty

        Returns:
            [Boolean]: 'True' if the size of the stack is 0, 'False' else
        """
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
    Implementation of the Depth-First Search algorithm. 
    Its purpose is to find a path from the source to the target through the Graph, dealing with flow and capacity constraints

    Args:
        Graph ([class Graph]): Contains the graph on which the algorithm will be applied
        source ([Node]): Initial node of the path 
        target ([Node]): Final node of the path 
        flow ([Dictionary]): Associates to each edge the current flow
        capacity ([Dictionary]): Associates to each edge the maximum supported flow

    Returns:
        [List]: List giving a correct path (according to the constraints of flow and capacity) from the source to the target
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


def FordFulkerson(Graph, source, well, disp_flow=False, not_explored_node_color="grey!50", default_edge_color="black", begin_border_color="red!50", end_border_color="red!50", current_edge_color="green", saturated_edge_color="red!25", saturated_edge_option="dashed"):
    """
    Application of the Ford-Fulkerson algorithm, to find the maximum flow from the source node to the target.
    Actually, this specific function colors and changes labels of the graph to illustrate the algorithm.
    It returns a list containing the different states of the graph.

    Args:
        Graph (class Graph): The graph on which the algorithm will be applied.
        source (String): Name of the source node. The graph must admit a "source node", it says a node from which there are only outgoing edges.
        well (String): Name of the well node. The graph must admit a "well node", it says a node from which there are only incoming edges
        disp_flow (bool, optional): If True, displays the maximum flow of the graph in the shell. Defaults to False.
        not_explored_node_color (str, optional): Color for nodes that have not already been explored. Defaults to "grey!50".
        default_edge_color (str, optional): Standard color for edges, when they are not explored. Defaults to "black".
        begin_border_color (str, optional): Color of the border surrounding the initial node. Defaults to "red!50".
        end_border_color (str, optional): Color of the border surrounding the final node. Defaults to "red!50".
        current_edge_color (str, optional): Color of the edges in the chosen path. Defaults to "green".
        saturated_edge_color (str, optional): Color of the saturated edges. Defaults to "red!25".
        saturated_edge_option (str, optional): Option to distinguish the saturated edges. Defaults to "dashed".

    Returns:
        [List]: List containing the differents states of the graph, like "frames". Each time a change is made, a copy of the graph is saved in the list.
    """
    # Dictionaries indexed by the edges. 
    # Capacity will not be changed during the execution. 
    # Flow is first set to 0, and during the algorithm it will stock the values of the flows on each edge
    flow = {arete : 0 for arete in Graph.E}
    capacity = {arete : int(Graph.edge_label[arete]) for arete in Graph.E}
    # List containing the differents states of the graph
    graph_list = []

    Graph_copy = Graph.copy()
    # Default syntax values
    for v in Graph_copy.V:
        Graph_copy.fill[v] = not_explored_node_color
    for e in Graph_copy.E:
        Graph_copy.color[e] = default_edge_color
    Graph_copy.contour_color[source] = begin_border_color
    Graph_copy.contour_color[well] = end_border_color
    graph_list.append(Graph_copy.copy())

    better_way_nodes = depthFirstSearch(Graph_copy, source, well, flow, capacity)
    while(better_way_nodes): # While the depthFirstSearch function finds a path through the graph
        if DEBUG:
            print("=" * 50)
            print("Chosen path: ", better_way_nodes)
            print("Flows before execution: ", flow)
        better_way_edges = [] # The depthFirstSearch function returns a sequence of nodes, that must be transformed into a sequence of edges
        for i in range(len(better_way_nodes) - 1):
            better_way_edges.append((better_way_nodes[i],better_way_nodes[i+1]))
        
        edges_to_increase = []
        edges_to_lower = []
        for edge in better_way_edges:
            if edge in Graph_copy.E:
                # If the edge is in the graph, its current flow will be increased
                edges_to_increase.append(edge)
            elif (edge[1], edge[0]) in Graph_copy.E:
                # If the edge is in the graph but in the opposite direction, its current flow will be lowered
                edges_to_lower.append((edge[1], edge[0]))

        for e in edges_to_increase + edges_to_lower:
            Graph_copy.color[e] = current_edge_color # The edges in the chosen path are coloured
        graph_list.append(Graph_copy.copy())            
        
        flow_of_way = min([capacity[e] - flow[e] for e in edges_to_increase] + [flow[e] for e in edges_to_lower])

        # Increasing or lowering flow on edges
        for e in edges_to_increase:
            flow[e] += flow_of_way
        for e in edges_to_lower:
            flow[e] -= flow_of_way

        for e in Graph_copy.E:
            Graph_copy.edge_label[e] = str(capacity[e] - flow[e])
        graph_list.append(Graph_copy.copy())

        for e in Graph_copy.E:
            if(capacity[e] - flow[e] == 0):
                Graph_copy.edge_options[e] = saturated_edge_option
                Graph_copy.color[e] = saturated_edge_color
            else:
                Graph_copy.color[e] = default_edge_color

        graph_list.append(Graph_copy.copy())

        if DEBUG:
            print("Flows after execution: ", flow)
            print("Capacities :", capacity)

        better_way_nodes = depthFirstSearch(Graph_copy, source, well, flow, capacity)

    # Computing the maximum flow accepted by the graph. By default it is not displayed, but it can be if the user sets disp_flow to 'True'
    max_flow = 0
    successors = getSuccessors(Graph_copy, source)
    for neighbour in successors:
        max_flow += flow[(source, neighbour)]
    if disp_flow: print("Maximum flow : ", max_flow)

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
def Floyd_Warshall(Graph, exploration_color='red', is_being_modified_color='green', has_been_modified_color='pink', bend=''):
    """This algorythm gives the shortest distance between every node of the graph.
    Beware ! This algorythm does not work the same way for an oriented and not oriented graph, in an oriented graph : non oriented edges will be converted to double arcs, not beautifully.

    Args:
        Graph (Graph): The Graph to explore
        exploration_color (str, optional): The color given to edges being tested as shortcuts. Defaults to 'red'.
        is_being_modified_color (str, optional): The color given to edges being modified. Defaults to 'green'.
        has_been_modified_color (str, optional): The color given to edges which has been modified . Defaults to 'pink'.
        bend (str, optional): 'right' or 'left': bend the new edges created. defaults to ''

    Returns:
        list(Graph): The list of each state of the graph during the application of the algorythm
    """
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
                        if bend: Graph.edge_options[path] += ",bend "+bend
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
                print(shortcut1)
                print(Graph.edge_label[shortcut1])
                print(shortcut2)
                print(Graph.edge_label[shortcut2])
                dist=str(int(Graph.edge_label[shortcut1])+int(Graph.edge_label[shortcut2]))
                tmp_color1=Graph.color[shortcut1]
                tmp_color2=Graph.color[shortcut2]
                tmp_contour=Graph.contour_color[k]
                Graph.color[shortcut1]=exploration_color
                Graph.color[shortcut2]=exploration_color
                Graph.contour_color[k]=exploration_color
                modified =False
                if path not in Graph.edge_label.keys() or int(Graph.edge_label[path]) > int(dist):
                    Graph.edge_label[path] = dist
                    Graph.color[path]=is_being_modified_color
                    modified = True
                liste_graphes.append(Graph.copy())
                Graph.color[shortcut1]=tmp_color1
                Graph.color[shortcut2]=tmp_color2
                Graph.contour_color[k]=tmp_contour
                if not tmp_contour:
                    Graph.contour_color.pop(k)
                if modified: Graph.color[path]=has_been_modified_color
    liste_graphes.append(Graph)
    return liste_graphes

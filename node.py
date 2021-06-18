
class Node:
    def __init__(self,name,color,label):
        """Create one node with few parameters 

        Args:
            name (string): name or numbers
            color (string): color of node
            label (string): annatotion side of node 
        """
        self.name = name
        self.color = color
        self.label = label
        self.successor = []

    def addSuccessor(self,node):
        self.successor.append(node)


class Link:
    def __init__(self,N1,N2,weigth,edge,color):
        """ link between two node 

        Args:
            N1 (Node): first node
            N2 (Node): second node
            weigth (int): weight of arc or edge
            edge (boolean): choose if it's an edge
            color (string): colors of arc or edge
        """
        self.node1 = N1
        self.node2 = N2
        self.weight = weigth
        self.edge = edge # true or false
        self.color = color



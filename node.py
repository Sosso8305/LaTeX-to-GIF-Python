
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

    def addSuccessor(node):
        self.successor.append(node)


class Link:
    def __init__(self,N1,N2,weigth,arrow,color):
        self.node1 = N1
        self.node2 = N2
        self.weight = weigth
        self.arrow = arrow # true or false
        self.color = color



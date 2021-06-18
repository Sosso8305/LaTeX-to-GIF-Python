import node

class Graph:
    def __init__(self,name):
        self.name = name
        self.allNodes = set() #mathematical set for don't have twice times one node
        self.allLinks = []

    def addLink(self,link):
        self.allNodes.append(link.node1)
        self.allNodes.append(link.node2)
        self.allLinks.append(link)
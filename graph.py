from node import Node, Link

class Graph:
    def __init__(self,name,option_tikzpicture="", dependencies=""):
        self.name = name
        self.option_tikzpicture = option_tikzpicture
        self.dependencies = dependencies
        self.allNodes = set() #mathematical set for don't have twice times one node
        self.allLinks = []

    def addLink(self,link):
        self.allNodes.add(link.node1)
        self.allNodes.add(link.node2)
        self.allLinks.append(link)

    def addOnlyLink(self,link):
        self.allLinks.append(link)

    def addNode(self,node):
        self.allNodes.add(node)

    def copyTo(self):
        from copy import deepcopy
        return deepcopy(self)

    def writeLaTeX(self):
        """AllCommand = []
        AllCommand.append("\\begin{tikzpicture} ["+self.option_tikzpicture+']')
        
        #Loop node
        for x in self.allNodes :
            if x==Node.name :
                AllCommand.append("\\node ("+Node.name+") ["+Node.options+"] {"+Node.name+"};")
        
        #Loop path
        i=0
        while i < len(self.allNodes) :
            if self.allLinks[i]==Link.name :
                AllCommand.append("\\path ("+Link.node1+") edge["+Link.other_options+"] ("+Link.node2+");")
            i+=1
        
        AllCommand.append("\\end{tikzpicture}")
        AllCommand = '\n'.join(AllCommand)
        
        return AllCommand"""
        return "toto \n"
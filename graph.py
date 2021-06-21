from node import Node, Link

class Graph:
    def __init__(self,name,option_tikzpicture="", dependencies=""):
        self.name = name
        self.option_tikzpicture = option_tikzpicture
        self.dependencies = dependencies
        self.allNodes = set() #mathematical set for don't have twice times one node
                                #set are not ordered : graphs may change each frame
        self.allLinks = []

    def addLink(self,link):
        self.allNodes.add(link.node1) #pourquoi ?
        self.allNodes.add(link.node2) #pourquoi ?
        self.allLinks.append(link)

    def addOnlyLink(self,link):
        self.allLinks.append(link)

    def addNode(self,node):
        self.allNodes.add(node)

    def copyTo(self):
        from copy import deepcopy
        return deepcopy(self)

    def getLink(self, n1, n2):
        for link in self.allLinks:
            if (link.node1 is n1) and (link.node2 is n2):
                return link

    def writeLaTeX(self):
        AllCommand = []
        AllCommand.append(f"\\begin{{tikzpicture}} [{self.option_tikzpicture}]")
        
        #Loop node
        for n in self.allNodes :
            command = f"\\node ({n.name}) ["
            if n.options != "":
                command += n.options
            if n.color != "":
                command += f",fill={n.color}"
            if n.label != "":
                command += f",label={n.label}"
            command+= f"] {{{n.name}}};"
            AllCommand.append(command)
        
        #Loop path
        for l in self.allLinks :
            command = f"\\path ({l.node1.name}) edge["
            if l.other_options != "":
                command += f"{l.other_options},"
            command += f"{'--' if l.edge else '->'}"
            command += ',"' + l.weight + '"'
            if l.color != "":
                command += f",color={l.color}"
            command += f"] ({l.node2.name});"
            AllCommand.append(command)
        
        AllCommand.append("\\end{tikzpicture}")
        AllCommand = '\n'.join(AllCommand)
        
        return AllCommand

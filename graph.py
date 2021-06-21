class Graph:
    def __init__(self,name,E=[], V=[], tikzpicture_option="", dependencies="", orientation={}):
        self.name = name
        self.tikzpicture_option = tikzpicture_option
        self.dependencies = dependencies
        self.E = E
        self.fill = {}
        self.label = {}
        self.node_options = {}
        self.V = V
        self.orientation = orientation
        self.weight = {}
        self.color = {}
        self.edge_options = {}

    def add_node(self,name,fill='', label='', node_options=''):
        self.E.append(name)
        if fill: self.fill[name]=fill
        if label: self.label[name]=label
        if node_options: self.node_options[name]=node_options

    def add_link(self, edge, orientation, weight='', color='', edge_options=''):
        if not edge[0] in self.E: self.E.append(edge[0])
        if not edge[1] in self.E: self.E.append(edge[1])
        self.V.append(edge)
        self.orientation[edge] = orientation
        if weight: self.weight[edge] = weight
        if color: self.color[edge] = color
        if edge_options: self.edge_options[edge]= edge_options

    def copy(self):
        from copy import deepcopy
        return deepcopy(self)

    def writeLaTeX(self):
        AllCommand = []
        AllCommand.append(f"\\begin{{tikzpicture}} [{self.tikzpicture_option}]")
        
        #Loop node
        for e in self.E :
            command = f"\\node ({e}) ["
            if self.node_options[e] != "":
                command += n.options + ','
            if n.color != "":
                command += f"fill={n.color},"
            if n.label != "":
                command += f"label={n.label},"
            command+= f"] {{{e}}};"
            AllCommand.append(command)
        
        #Loop path
        for v in self.V :
            command = f"\\path ({v[0]}) edge["
            if self.edge_options[v] != "":
                command += f"{self.edge_options[v]},"
            command += f"{self.orientation[v]},"
            if self.weight[v] != '':
                command += '"' + self.weight[v] + '",'
            if self.color[v] != "":
                command += f"color={self.color[v]},"
            command += f"] ({v[1]});"
            AllCommand.append(command)
        
        AllCommand.append("\\end{tikzpicture}")
        AllCommand = '\n'.join(AllCommand)
        
        return AllCommand

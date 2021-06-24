from collections import defaultdict


class Graph:
    def __init__(self,name,V, E, orientation, preambule=""):
        self.name = name
        self.V = V
        self.E = E

        self.preambule =preambule

        #option out for V
        self.fill = defaultdict(lambda: '')
        self.label = defaultdict(lambda: '')
        self.node_options = defaultdict(lambda: '')
        self.display_name = defaultdict(lambda: '')
        self.coordonnee = defaultdict(lambda: '')
        self.label_color = defaultdict(lambda: '')
        self.label_position = defaultdict(lambda: '')
        self.contour = defaultdict(lambda: '')

        #option out for E
        self.orientation = orientation
        self.weight = defaultdict(lambda: '')
        self.color = defaultdict(lambda: '')
        self.edge_options = defaultdict(lambda: '')

    def add_node(self,id, display_name, fill='', label='', node_options='', coordonnee=(), label_color='', label_position='', contour=''):
        self.V.append(id)
        self.display_name[id] = display_name
        if fill: self.fill[id]=fill
        if label: self.label[id]=label
        if node_options: self.node_options[id]=node_options
        if coordonnee: self.coordonnee[id]=coordonnee
        if label_color: self.label_color[id]=label_color
        if label_position: self.label_position[id]=label_position
        if contour: self.contour[id] = contour

    def add_link(self, edge, orientation, weight='', color='', edge_options=''):
        if not edge[0] in self.V: self.V.append(edge[0])
        if not edge[1] in self.V: self.V.append(edge[1])
        self.E.append(edge)
        self.orientation[edge] = orientation
        if weight: self.weight[edge] = weight
        if color: self.color[edge] = color
        if edge_options: self.edge_options[edge]= edge_options

    def copy(self):
        from copy import deepcopy
        return deepcopy(self)

    def writeLaTeX(self):
        AllCommand = []
        
        #Loop node
        for v in self.V :
            command = f"\\node ({v}) "
            if v in self.coordonnee.keys():
                command += f"at({self.coordonnee[v][0]},{self.coordonnee[v][1]}) ["
            else: command += "["
            if v in self.node_options.keys():
                command += self.node_options[v] + ','
            if v in self.fill.keys():
                command += f"fill={self.fill[v]},"
            if v in self.label.keys():
                command += f"label={{"
                if v in self.label_color.keys():
                    command += f"[{self.label_color[v]}]"
                if v in self.label_position.keys():
                    command += f"{self.label_position[v]}"
                command += f":{self.label[v]}}},"
            if v in self.contour.keys():
                command += f"draw={self.contour[v]}"
            command+= f"] {{{self.display_name[v]}}};"
            AllCommand.append(command)
        
        #Loop path
        for e in self.E :
            command = f"\\path ({e[0]}) edge["
            if e in self.edge_options.keys():
                command += f"{self.edge_options[e]},"
            command += f"{self.orientation[e]},"
            if e in self.weight.keys():
                command += '"' + self.weight[e] + '",'
            if e in self.color.keys():
                command += f"color={self.color[e]},"
            command += f"] ({e[1]});"
            AllCommand.append(command)
        
        AllCommand = '\n'.join(AllCommand)
        
        return AllCommand


#########################################################
######################## GETTER #########################
#########################################################

@property
def V(self):
    return self.V

@property
def E(self):
    return self.E


#########################################################
######################## SETTER #########################
#########################################################

@V.setter
def V(self, new_list_V):
    self.V = new_list_V

@E.setter
def E(self, new_list_E):
    self.E = new_list_E




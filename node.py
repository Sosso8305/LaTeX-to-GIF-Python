
class Node:
    def __init__(self,name):
        self.name = name


class Link:
    def __init__(self,N1,N2,weigth,arrow):
        self.node1 = N1
        self.node2 = N2
        self.weight = weigth
        self.arrow = arrow # true or false

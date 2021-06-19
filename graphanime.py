from graph import Graph
from node import Node, Link

def load(file):
    fileTex = open(file,"r")

    G = Graph("G")

    lines = fileTex.readlines()
    

    for line in lines:

        line= ''.join(line.split())


        if line.find("\\node") != -1:
            options = line[(line.find("[")+1):line.find("]")]
            options = options.split(sep=",")

            
            opt_del=[]
            for opt in options:
                if opt.find("fill") != -1:
                    fill = opt[5:]
                    opt_del.append(opt)
                    

                elif opt.find("label") != -1:
                    label = opt[6:]
                    opt_del.append(opt)
                    
         
            options = [x for x in options if x not in opt_del]

            options = ",".join(options)
            
            str_node = line[(line.find("(")+1):line.find(")")] 
            globals()[str_node]= Node(line[(line.find("{")+1):line.find("}")],fill,label,options)

            G.addNode(globals()[str_node])
            continue


        if line.find("\\path") != -1:
            print("TODO")
    


def Dijkstra(Graph,source,sink):
    print("TODO")


load("LaTeX/Text.tex")
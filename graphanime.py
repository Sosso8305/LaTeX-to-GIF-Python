from graph import Graph
from node import Node, Link

def load(file):
    fileTex = open(file,"r")

    fragTexts = fileTex.readline()
    for text in fragTexts:
        i=0
        while i<len(text):
            if text[i] == '%':
                text = text[0:i]

    allText = ''.join(fragTexts)

    AllCommand  = allText[allText.find("\\begin{tikzpicture}"):allText.find("\\end{tikzpicture}")]

    print(AllCommand)

    # for command in AllCommand:

    #     command= ''.join(command.split())


    #     if command.find("\\node") != -1:
    #         options = command[(command.find("[")+1):command.find("]")]
    #         options = options.split(sep=",")

            
    #         opt_del=[]
    #         for opt in options:
    #             if opt.find("fill") != -1:
    #                 fill = opt[5:]
    #                 opt_del.append(opt)
                    

    #             elif opt.find("label") != -1:
    #                 label = opt[6:]
    #                 opt_del.append(opt)
                    
         
    #         options = [x for x in options if x not in opt_del]

    #         options = ",".join(options)
            
    #         str_node = command[(command.find("(")+1):command.find(")")] 
    #         globals()[str_node]= Node(command[(command.find("{")+1):command.find("}")],fill,label,options)

    #         G.addNode(globals()[str_node])
    #         continue


    #     if command.find("\\path") != -1:
    #         endNameFirstNode =command.find(")")
    #         str_node1 = command[(command.find("(")+1):endNameFirstNode]
    #         str_node2 = command[(endNameFirstNode+1):]
    #         str_node2 = str_node2
    #         print(str_node1,str_node2)
            
    


def Dijkstra(Graph,source,sink):
    print("TODO")


load("LaTeX/Text.tex")
from graph import Graph
from node import Node, Link

def load(file):
    fileTex = open(file,"r")

    # Remove comments
    fragTexts = fileTex.readlines()
    line =[]
    for text in fragTexts:
        if text.find('%') !=-1:
            text = text[:text.find('%')]
            text += '\n'
        line.append(text)
    allText = ''.join(line)

    # Get the uspackage&uselibrary lines
    dependencies = allText[allText.find("\\documentclass[tikz]{standalone}")+len('\documentclass[tikz]{standalone}'):allText.find("\\begin{document}")]

    AllCommand  = allText[allText.find("\\begin{tikzpicture}"):allText.find("\\end{tikzpicture}")]
    end_option_tikzpicture = AllCommand.find("]")
    option_tikzpicture = AllCommand[AllCommand.find("["):end_option_tikzpicture]
    AllCommand = AllCommand[(end_option_tikzpicture+1):]
    
    G= Graph("G", option_tikzpicture, dependencies)

    AllCommand = AllCommand.split(';')


    for command in AllCommand:

        command= ''.join(command.split()) # Removes spaces


        if command.find("\\node") != -1:
            options = command[(command.find("[")+1):command.find("]")]
            options = options.split(',')

            exist_fill=0
            exist_label=0
            opt_del=[]
            for opt in options:
                if opt.find("fill") != -1:
                    fill = opt[5:]
                    opt_del.append(opt)
                    exist_fill=1
                    

                elif opt.find("label") != -1:
                    label = opt[6:]
                    opt_del.append(opt)
                    exist_label = 1
                    
            if not exist_fill:
                fill = 0 #print(issubclass(fill.__class__, str)): false
            if not exist_label:
                label = 0 #print(issubclass(fill.__class__, str)): false
            options = [x for x in options if x not in opt_del]

            options = ",".join(options)
            
            str_node = command[(command.find("(")+1):command.find(")")] 
            globals()[str_node]= Node(command[(command.find("{")+1):command.find("}")],fill,label,options)

            G.addNode(globals()[str_node])
            continue


    #     if command.find("\\path") != -1:
    #         endNameFirstNode =command.find(")")
    #         str_node1 = command[(command.find("(")+1):endNameFirstNode]
    #         str_node2 = command[(endNameFirstNode+1):]
    #         str_node2 = str_node2
    #         print(str_node1,str_node2)
            
    
    print(G.allNodes)

def Dijkstra(Graph,source,sink):
    print("TODO")


load("LaTeX/Text.tex")
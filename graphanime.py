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
    Allpackage = allText[allText.find("\\documentclass[tikz]{standalone}"):allText.find("\\begin{document}")]


    AllCommand  = allText[allText.find("\\begin{tikzpicture}"):allText.find("\\end{tikzpicture}")]
    end_option_tikzpicture = AllCommand.find("]")
    option_tikzpicture = AllCommand[AllCommand.find("["):end_option_tikzpicture]
    AllCommand = AllCommand[(end_option_tikzpicture+1):]
    
    G= Graph("G", option_tikzpicture, Allpackage)

    AllCommand = AllCommand.split(';')


    for command in AllCommand:

        command= ''.join(command.split())


        if command.find("\\node") != -1:
            options = command[(command.find("[")+1):command.find("]")]
            options = options.split(',')

            
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
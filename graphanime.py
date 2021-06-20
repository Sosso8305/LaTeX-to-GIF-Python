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

            opt_del=[]
            fill = 0 #print(issubclass(fill.__class__, str)): false
            label = 0 #print(issubclass(label.__class__, str)): false
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


        if command.find("\\path") != -1:
            endNameFirstNode =command.find(")")
            str_node1 = command[(command.find("(")+1):endNameFirstNode]
            str_node2 = command[(endNameFirstNode+1):]
            str_node2 = str_node2[(str_node2.find("(")+1):str_node2.find(")")]
            

            options = command[(command.find("[")+1):command.find("]")]
            options = options.split(',')

            opt_del=[]
            color=0 #print(issubclass(color.__class__, str)): false
            weight='1'
            for opt in options:
                if opt.find("-") != -1:
                    edge = (opt.find("--") != -1)
                    opt_del.append(opt)

                elif opt.find("color") != -1:
                    color = opt[6:]
                    opt_del.append(opt)

                elif opt.find("weight") != -1:
                    weight = opt[7:]
                    opt_del.append(opt)

            options = [x for x in options if x not in opt_del]

            options = ",".join(options)
            
            G.addLink(Link(globals()[str_node1],globals()[str_node2],weight,edge,color,options))

    return G


def Dijkstra(Graph,source,sink):
    print("TODO")


def genpdf(anim,file):
    
    fOut = open(file+".tex","a")

    fOut.write("\\documentclass{beamer} \n")
    fOut.write( anim[0].dependencies + "\n")
    fOut.write("\\begin{document} \n")

    for G in anim:
        fOut.write("\\begin{frame} \n")
        fOut.write(G.writeLaTeX())
        fOut.write("\\end{frame} \n")
    
    fOut.write("\\end{document}")




if __name__ == "__main__":

    load("LaTeX/Text.tex")

    A = [load('LaTeX/Text.tex'), load('LaTeX/Test.tex')]

    genpdf(A,"LaTex/first")


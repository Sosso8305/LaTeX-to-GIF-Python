from heapq import heappop, heappush
from graph import Graph
from node import Node, Link

# Define constants as in pseudo-code
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
INFINI = 1000000

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
    option_tikzpicture = AllCommand[AllCommand.find("[")+1:end_option_tikzpicture]
    AllCommand = AllCommand[(end_option_tikzpicture+1):]
    
    G= Graph("G", option_tikzpicture, dependencies)

    AllCommand = AllCommand.split(';')


    for command in AllCommand:

        command= ''.join(command.split()) # Removes spaces 
        #WIP some options may need spaces?


        if command.find("\\node") != -1:
            options = command[(command.find("[")+1):command.find("]")]
            options = options.split(',')

            opt_del=[]
            fill ="" 
            label ="" 
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
            color="" 
            weight='1'
            for opt in options:
                if opt.find("-") != -1:
                    edge = (opt.find("--") != -1)
                    opt_del.append(opt)

                elif opt.find("color") != -1:
                    color = opt[6:]
                    opt_del.append(opt)

                elif opt.find('"') != -1:
                    weight = opt[1:-1]
                    opt_del.append(opt)

            options = [x for x in options if x not in opt_del]

            options = ",".join(options)
            
            G.addLink(Link(globals()[str_node1],globals()[str_node2],weight,edge,color,options))

    return G


def Dijkstra(Graph,source,sink):
    print("TODO")
    relative_distance = 0
    distance_from_source = 0
    priority_queue = []
    for s in Graph.allNodes:
        s.color = WHITE
        s.label = str(INFINI) # Il me faut un nombre assez grand pour simuler l'infini
    heappush(priority_queue, (source, 0)) # Je mets dans ma file de priorités un tuple avec le noeud source et la valeur 0 (car distance de source à source = 0)
    source.couleur = GREY
    source.label = str(0) # Le label tel que défini dans la classe Node contient la distance depuis le noeud source
    while(priority_queue):
        (noeud, distance_from_source) = heappop(priority_queue)
        noeud.couleur = GREY
        for s in noeud.successors:
            lien = Graph.getLink(noeud, s) # Obtient le lien entre le noeud actuellement étudié et son voisin
            if distance_from_source + lien.weight < int(s.label): # Comme le label est un string, il faut le passer en int
                s.label = str(distance_from_source + lien.weight)
                s.predecessors.append(noeud)
                heappush(priority_queue, (s, int(s.label)))
        noeud.couleur = BLACK




def genpdf(anim,file):
    
    fOut = open(file+".tex","w")

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

    A = [load('LaTeX/Text.tex'), load('LaTeX/Text.tex')]

    genpdf(A,"LaTeX/first")


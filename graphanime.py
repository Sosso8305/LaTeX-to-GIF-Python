from heapq import heappop, heappush
from graph import Graph

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
    
    G= Graph("G", [], [], tikzpicture_option=option_tikzpicture, dependencies=dependencies)

    AllCommand = AllCommand.split(';')
    for command in AllCommand:
        if command.find("\\node") != -1:
            options = command[(command.find("[")+1):command.find("]")]
            options = options.split(',')

            fill ="" 
            label ="" 
            other_options=[]
            for opt in options:
                if opt.find("fill") != -1:
                    opt=''.join(opt.split())
                    fill = opt[5:]

                elif opt.find("label") != -1:
                    opt=''.join(opt.split())
                    label = opt[6:]
                else:
                    other_options.append(opt)

            options = ",".join(other_options)
            
            name = command[(command.rfind("{")+1):command.rfind("}")] 

            G.add_node(name, fill=fill, label=label, node_options=options)

        elif command.find("\\path") != -1:
            command = command.splitlines()
            for c in command:
                if c.find('edge')==-1: continue
                edge=(c[c.find("(")+1:c.find(")")], c[c.rfind("(")+1:c.rfind(")")])
                options = c[(c.find("[")+1):c.find("]")]
                options = options.split(',')

                other_options=[]
                color="" 
                weight=''
                for opt in options:
                    if opt.find("-") != -1:
                        opt=''.join(opt.split())
                        orientation = opt

                    elif opt.find("color") != -1:
                        opt=''.join(opt.split())
                        color = opt[6:]

                    elif opt.find('"') != -1:
                        opt=''.join(opt.split())
                        weight = opt[1:-1]

                options = ",".join(other_options)
                
                G.add_link(edge, orientation, weight=weight, color=color, edge_options=options)

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


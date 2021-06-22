from heapq import heappop, heappush
from graph import Graph
from pdflatex import PDFLaTeX
import os, platform, subprocess

# Define constants as in pseudo-code
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
INFINI = "$\infty$"

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
    preambule = allText[allText.find("\\documentclass[tikz]{standalone}")+len('\documentclass[tikz]{standalone}'):allText.find("\\begin{document}")]
    AllCommand  = allText[allText.find("\\begin{tikzpicture}"):allText.find("\\end{tikzpicture}")]
    end_option_tikzpicture = AllCommand.find("]")
    option_tikzpicture = AllCommand[AllCommand.find("[")+1:end_option_tikzpicture]
    AllCommand = AllCommand[(end_option_tikzpicture+1):]
    
    G= Graph("G", [], [], {}, option_tikzpicture, preambule)

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

            id = command[(command.find("(")+1):command.find(")")]
            name = command[(command.rfind("{")+1):command.rfind("}")]

            coordonnee = ()
            if command.find("at(") != -1: 
                coordonnee = command[command.find("at(")+3:command.find("at(")+command[command.find("at("):].find(")")]
                coordonnee = coordonnee.split(',')
            G.add_node(id, name, fill=fill, label=label, node_options=options, coordonnee=coordonnee)

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
    Graph_copy = Graph.copyTo()
    liste_graphes = []
    distance_from_source = 0
    priority_queue = []
    for s in Graph_copy.allNodes:
        s.color = WHITE
        s.label = INFINI # Il me faut un nombre assez grand pour simuler l'infini
    heappush(priority_queue, (source, 0)) # Je mets dans ma file de priorités un tuple avec le noeud source et la valeur 0 (car distance de source à source = 0)
    source.label = str(0) # Le label tel que défini dans la classe Node contient la distance depuis le noeud source
    liste_graphes.append(Graph_copy.copyTo())
    source.couleur = GREY
    liste_graphes.append(Graph_copy.copyTo())

    while(priority_queue):
        (noeud, distance_from_source) = heappop(priority_queue)
        noeud.couleur = GREY
        liste_graphes.append(Graph_copy.copyTo())
        
        for s in noeud.successors:
            lien = Graph_copy.getLink(noeud, s) # Obtient le lien entre le noeud actuellement étudié et son voisin
            lien.color = ORANGE
            liste_graphes.append(Graph_copy.copyTo())
            if (s.label == INFINI) or (distance_from_source + lien.weight < int(s.label)): # Comme le label est un string, il faut le passer en int
                s.label = str(distance_from_source + lien.weight)
                liste_graphes.append(Graph_copy.copyTo())
                s.predecessors.append(noeud)
                heappush(priority_queue, (s, int(s.label)))
        noeud.couleur = BLACK
        liste_graphes.append(Graph_copy.copyTo())
    
    return liste_graphes

def FunctTest(Graph):
    i = 0
    j = 0
    for s in Graph.V:
        if(i%3 == 0):
            Graph.fill[s] = "red"
        elif(i%3 == 1):
            Graph.label[s] = "STI > toutes les autres filieres"
        else:
            Graph.label[s] = "TA XD GER SZ"
            Graph.fill[s] = "green"
        i += 1
    for a in Graph.E:
        if(j%2 == 0):
            Graph.color[a] = "blue"
        else:
            Graph.weight[a] = "42"
        j += 1
    return "FunctTest\n"



def genpdf(anim,file):

    #Python to LaTeX
    if not os.path.exists("./out/"):
        os.mkdir("./out/")
    os.chdir("./out/")
    
    fOut = open(file+".tex","w")

    fOut.write("\\documentclass{beamer} \n")
    fOut.write( anim[0].preambule + "\n")
    fOut.write("\\begin{document} \n")

    for G in anim:
        fOut.write("\\begin{frame} \n")
        fOut.write(G.writeLaTeX())
        fOut.write("\\end{frame} \n")
    
    fOut.write("\\end{document}")

    fOut.close()
    
    ######LaTeX to PDF
    
    # TeX source filename
    tex_filename = file + '.tex'
    filename, ext = os.path.splitext(tex_filename)
    # the corresponding PDF filename
    pdf_filename = file + '.pdf'

    # compile TeX file
    subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename])

    # check if PDF is successfully generated
    if not os.path.exists(pdf_filename):
        raise RuntimeError('PDF output not found')

    # open PDF with platform-specific command
    if platform.system().lower() == 'darwin':
        subprocess.run(['open', pdf_filename])
    elif platform.system().lower() == 'windows':
        os.startfile(pdf_filename)
    elif platform.system().lower() == 'linux':
        subprocess.run(['xdg-open', pdf_filename])
    else:
        raise RuntimeError('Unknown operating system "{}"'.format(platform.system()))

    """pdfl = PDFLaTeX.from_texfile("first.tex")
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
    """
    os.chdir("../")


if __name__ == "__main__":

    x = load('LaTeX/Text.tex')
    FunctTest(x)
    A = [load('LaTeX/Text.tex'), x]

    genpdf(A,"first")


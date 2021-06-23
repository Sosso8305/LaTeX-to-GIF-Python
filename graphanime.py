from heapq import heappop, heappush
from graph import Graph
import os, platform, subprocess, tempfile



############Begin_Parser##################

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
    AllCommand  = allText[allText.find("\\begin{tikzpicture}") + len("\\begin{tikzpicture}"):allText.find("\\end{tikzpicture}")]
    
    G= Graph("G", [], [], {}, preambule)

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

############END_Parser##################



#############BEGIN_Back-end###################

def gen_beamer(anim,file,out_tex=False):

    ######Python to LaTeX######
    if not os.path.exists("./out/"):
        os.mkdir("./out/")
    os.chdir("./out/")

    current_dir = os.getcwd()

    with tempfile.TemporaryDirectory() as tempdir:
     
        os.chdir(tempdir)
        fOut = open(file+".tex","w")
        
        fOut.write("\\documentclass{beamer} \n")
        fOut.write( anim[0].preambule + "\n")
        fOut.write("\\tikzset{%https://tex.stackexchange.com/questions/49888/tikzpicture-alignment-and-centering\n") #source
        fOut.write("master/.style={\nexecute at end picture={\n\coordinate (lower right) at (current bounding box.south east);\n\coordinate (upper left) at (current bounding box.north west);}},")
        fOut.write("slave/.style={\nexecute at end picture={\n\pgfresetboundingbox\n\path (upper left) rectangle (lower right);}}}\n")

        fOut.write("\\begin{document} \n")

        first=True
        for G in anim:
            fOut.write("\\begin{frame} \n")
            fOut.write("\\centering\n")
            fOut.write("\\begin{tikzpicture} ")
            if first:
                fOut.write("[master]\n")
                first=False
            else: fOut.write("[slave]\n")
            fOut.write(G.writeLaTeX())
            fOut.write("\\end{tikzpicture} \n")
            fOut.write("\\end{frame} \n")
        
        fOut.write("\\end{document}")

        fOut.close()
    
        ######LaTeX to PDF######
        
        # TeX source filename
        tex_filename = os.path.join(tempdir,file+".tex")
        # the corresponding PDF filename
        pdf_filename = os.path.join(tempdir,file+".pdf")

        # compile TeX file
        subprocess.run(['pdflatex', '-interaction=batchmode', tex_filename])

        os.chdir(current_dir)

        # check if PDF is successfully generated
        if os.path.exists(pdf_filename):
            if (platform.system()=='Windows'):
                os.system('copy ' + pdf_filename + ' "' +current_dir + '\\"')
                if(out_tex):
                    os.system('copy ' + tex_filename + ' "' +current_dir + '\\"')

            elif(platform.system()=='Linux'or'Darwin'):
                subprocess.run(['cp', pdf_filename, file+".pdf"])
                if(out_tex):
                    subprocess.run(['cp', tex_filename, file+".tex"])

            else:
                print("Don't have a right system")

        else:
            raise RuntimeError('PDF output not found')


        os.chdir("../")

    


def gen_pdf(anim,file,out_tex=False):
    
    ######Python to LaTeX######
    if not os.path.exists("./out/"):
        os.mkdir("./out/")
    os.chdir("./out/")

    current_dir = os.getcwd()

    with tempfile.TemporaryDirectory() as tempdir:
     
        os.chdir(tempdir)
        fOut = open(file+".tex","w")
        
        fOut.write("\\documentclass[tikz]{standalone}\n")
        fOut.write( anim[0].preambule + "\n")
        
        fOut.write("\\begin{document} \n")

        for G in anim:
            
            fOut.write("\\centering\n")
            fOut.write("\\begin{tikzpicture} ")
            fOut.write(G.writeLaTeX())
            fOut.write("\\end{tikzpicture} \n")
           
        
        fOut.write("\\end{document}")

        fOut.close()
    
        ######LaTeX to PDF######
        
        # TeX source filename
        tex_filename = os.path.join(tempdir,file+".tex")
        # the corresponding PDF filename
        pdf_filename = os.path.join(tempdir,file+".pdf")

        # compile TeX file
        subprocess.run(['pdflatex', '-interaction=batchmode', tex_filename])

        os.chdir(current_dir)

        # check if PDF is successfully generated
        if os.path.exists(pdf_filename):
            if (platform.system()=='Windows'):
                os.system('copy ' + pdf_filename + ' "' +current_dir + '\\"')
                if(out_tex):
                    os.system('copy ' + tex_filename + ' "' +current_dir + '\\"')

            elif(platform.system()=='Linux'or'Darwin'):
                subprocess.run(['cp', pdf_filename, file+".pdf"])
                if(out_tex):
                    subprocess.run(['cp', tex_filename, file+".tex"])

            else:
                print("Don't have a right system")

        else:
            raise RuntimeError('PDF output not found')


        os.chdir("../")
    

#############END_Back-end###################

if __name__ == "__main__":

    x = load('LaTeX/Text.tex')
    FunctTest(x)
    A = [load('LaTeX/Text.tex'), x]

    gen_beamer(A,"first")
    gen_pdf(A, "second",True)


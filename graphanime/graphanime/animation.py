from .graph import Graph
from pdf2image import convert_from_path
from apng import APNG
from PIL import Image
import os, platform, subprocess, tempfile, glob, shutil


__all__ = ['load', 'gen_beamer', 'gen_pdf', 'gen_apng', 'gen_gif']

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
            options = command[(command.find("[")+1):command.rfind("]")]
            options = options.split(',')

            fill ="" 
            label ="" 
            label_color=""
            label_position=""
            contour_color=""
            other_options=[]
            for opt in options:
                if opt.find("fill") != -1:
                    if opt.find("=") != -1:
                        fill = " "+opt[opt.find("=")+1:]
                    else : fill = " "
                elif opt.find("label") != -1:
                    if opt.find("{") != -1:
                        opt=opt[opt.find("{")+1:opt.find("}")]
                    if opt.find(":") != -1:
                        label = opt[opt.find(":")+1:]
                        if opt.find("[") != -1:
                            label_color = opt[opt.find("[")+1:opt.find("]")]
                            label_position = opt[opt.find("]")+1:opt.find(":")]
                        else :
                            label_position = opt[:opt.find(":")]
                    else:
                        label=opt[opt.find("=")+1:]
                elif opt.find("draw") != -1:
                    if opt.find("=") != -1:
                        contour_color = " "+opt[opt.find("=")+1:]
                    else : contour_color = " "
                else:
                    other_options.append(opt)

            options = ",".join(other_options)

            id = command[(command.find("(")+1):command.find(")")]
            name = command[(command.rfind("{")+1):command.rfind("}")]

            coordonnee = ()
            if command.find("at(") != -1: 
                coordonnee = command[command.find("at(")+3:command.find("at(")+command[command.find("at("):].find(")")]
                coordonnee = coordonnee.split(',')
            G.add_node(id, name, fill=fill, label=label, node_options=options, coordonnee=coordonnee, label_color=label_color, label_position=label_position, contour_color=contour_color)

        elif command.find("\\path") != -1:
            command = command.splitlines()
            for c in command:
                if c.find('edge')==-1: continue
                edge=(c[c.find("(")+1:c.find(")")], c[c.rfind("(")+1:c.rfind(")")])
                options = c[(c.find("[")+1):c.find("]")]
                options = options.split(',')

                other_options=[]
                color="" 
                edge_label=''
                for opt in options:
                    if opt.find("color") != -1:
                        opt=''.join(opt.split())
                        color = opt[6:]
                    elif opt.find('"') != -1:
                        edge_label = opt[opt.find('"')+1:opt.rfind('"')]
                    elif opt.find("-") != -1:
                        opt=''.join(opt.split())
                        if opt=='-' or opt=='->' or opt=='<-':
                            orientation = opt
                    else:
                        other_options.append(opt)
                options = ",".join(other_options)
                
                G.add_link(edge, orientation, edge_label=edge_label, color=color, edge_options=options)
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
        print("Nom du fichier pdf : ", pdf_filename)
        if os.path.exists(pdf_filename):
            shutil.copy2(pdf_filename,current_dir)
            if(out_tex):
                shutil.copy2(tex_filename,current_dir)
            

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
        fOut.write("\\tikzset{%https://tex.stackexchange.com/questions/49888/tikzpicture-alignment-and-centering\n") #source
        fOut.write("master/.style={\nexecute at end picture={\n\coordinate (lower right) at (current bounding box.south east);\n\coordinate (upper left) at (current bounding box.north west);}},")
        fOut.write("slave/.style={\nexecute at end picture={\n\pgfresetboundingbox\n\path (upper left) rectangle (lower right);}}}\n")

        fOut.write("\\begin{document} \n")
        first = True
        for G in anim:
            fOut.write("\\centering\n")
            fOut.write("\\begin{tikzpicture}\n")
            if first:
                fOut.write("[master]\n")
                first=False
            else: fOut.write("[slave]\n")
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
            shutil.copy2(pdf_filename,current_dir)
            if(out_tex):
                shutil.copy2(tex_filename,current_dir)

        else:
            raise RuntimeError('PDF output not found')


        os.chdir("../")


def key_sort(word,file):
    return int(word[len(file)+1:-4])


def gen_gif(anim,file,duration=500):
    if not os.path.exists("./out/"):
        os.mkdir("./out/")
    os.chdir("./out/")    

    current_dir = os.getcwd()

    with tempfile.TemporaryDirectory() as tempdir:
        os.chdir(tempdir)
        gen_pdf(anim, file)
        
        pages = convert_from_path("./out/"+ file +".pdf")

        nb = 0
        for page in pages:
            nb+=1
            page.save(file+'_'+str(nb)+".png",'PNG')

       

        

        frames = []
        images = glob.glob("*.png")
        
        images= sorted(images, key= lambda x: key_sort(x,file))
        
        
        for img in images:
            new_frame =Image.open(img)
            frames.append(new_frame)
        for _ in range(5):
            frames.append(new_frame)

        frames[0].save(file+".gif",format='GIF',append_images=frames[1:],save_all=True,duration=duration,loop=0)
    

        # the corresponding GIF filename
        gif_filename = os.path.join(tempdir,file+".gif")


        os.chdir(current_dir)


        if os.path.exists(gif_filename):
            shutil.copy2(gif_filename,current_dir)


        os.chdir("../")
        

def gen_apng(anim,file,delay=500):
    if not os.path.exists("./out/"):
        os.mkdir("./out/")
    os.chdir("./out/")    

    current_dir = os.getcwd()

    with tempfile.TemporaryDirectory() as tempdir:
        os.chdir(tempdir)
        gen_pdf(anim, file)
        
        pages = convert_from_path("./out/"+ file +".pdf")

        nb = 0
        for page in pages:
            nb+=1
            page.save(file+'_'+str(nb)+".png",'PNG')
        for _ in range(5):
            nb +=1
            page.save(file+'_'+str(nb)+".png",'PNG')
        
        images = glob.glob("*.png")

        images= sorted(images, key= lambda x: key_sort(x,file))

        
        APNG.from_files(images,delay=delay).save(file+".png")
    

        # the corresponding GIF filename
        apng_filename = os.path.join(tempdir,file+".png")


        os.chdir(current_dir)


        if os.path.exists(apng_filename):
            shutil.copy2(apng_filename,current_dir)
        else:
            raise RuntimeError('APNG output not found')


        os.chdir("../")


            

    

#############END_Back-end###################




from tkinter import *
from tkinter import filedialog
import os
from modeller import *
from modeller.automodel import *


root = Tk()
root.title("MODELLER GUI")
root.geometry("1060x300")



def browsefunc1():
    global filename1
    filename1 = filedialog.askopenfilename()
    pathlabel1.config(text=filename1)
def browsefunc2():
    global filename2
    filename2 = filedialog.askopenfilename()
    pathlabel2.config(text=filename2)
def readfasta(filename):
    sequence = ""
    with open(filename, "r") as f:
        for line in f:
            if not line[0] == ">":
                sequence += line.rstrip()
    return sequence
def make_ali(file):
    seq = readfasta(file)
    line1 = ">P1;" + c.get() +"\n"
    line2 = "sequence:"+ c.get() +":::::::0.00: 0.00\n"
    line3 = seq + "*"
    ali_file = line1+line2+line3
    return ali_file
def pdb_pp(file):
    with open(file, "r") as f:
        lines = f.readlines()
    with open(file, "w") as f:
        for line in lines:
            if (line.startswith('ATOM') or line.startswith('TER')):
                f.write(line)
    return


def run():
    x = print(filename1)
    y = print(filename2)
    z = print(c.get())
    w = print(d.get())
    justname1 = os.path.basename(filename1).split(".") #fasta
    justname2 = os.path.basename(filename2).split(".") #protein
    onlyname1 = str(justname1[0])
    onlyname2 = str(justname2[0])
    print(justname1)
    print(justname2)
    print(onlyname1)
    print(onlyname2)
    content = make_ali(os.path.basename(filename1))
    f = open("align1.pir", "x")
    f.write(content)
    f.close()
    pdb_pp(os.path.basename(filename2))





    env = environ()
    aln = alignment(env)
    mdl = model(env, file= onlyname2, model_segment=('FIRST:A', 'LAST:A'))
    aln.append_model(mdl, align_codes= onlyname2 + "A", atom_files= os.path.basename(filename2))
    aln.append(file='align1.pir', align_codes= c.get())
    aln.align2d()
    aln.write(file=onlyname1 + "-" + onlyname2 + ".ali", alignment_format='PIR')


    a = automodel(env, alnfile= onlyname1 + "-" + onlyname2 + ".ali",
                  knowns=onlyname2 + "A", sequence= c.get(),
                  assess_methods=(assess.DOPE,
                                  # soap_protein_od.Scorer(),
                                  assess.GA341))
    a.starting_model = 1
    a.ending_model = int(d.get())
    a.make()

    return a.make()

browsebutton1 = Button(root, text="Browse", command=browsefunc1)
browsebutton1.grid(row=1, column=2, sticky=W)
pathlabel1 = Label(root)
pathlabel1.grid(row=1, column=3, sticky=W)
A = Label(root, text = "Select the FASTA file: ")
A.grid(row=1, column=1, sticky=W)


browsebutton2 = Button(root, text="Browse", command=browsefunc2)
browsebutton2.grid(row=2, column=2, sticky=W)
pathlabel2 = Label(root)
pathlabel2.grid(row=2, column=3, sticky=W)
B = Label(root, text = "Select the pdb file: ")
B.grid(row=2, column=1, sticky=W)


c = Entry(root, width = "25", textvariable= StringVar)
c.grid(row=3, column=2, sticky=W)
C = Label(root, text = "Enter an alignment code: ")
C.grid(row=3, column=1, sticky=W)


d = Entry(root, width = "25", textvariable= StringVar)
d.grid(row=4, column=2, sticky=W)
D = Label(root, text = "Enter the number of models to be generated:")
D.grid(row=4, column=1, sticky=W)


run_button = Button(root, text = "RUN", command = run).place(x = 280, y = 250)



root.mainloop()
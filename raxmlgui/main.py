#!/usr/bin/env python 
# raxmlGUI 1.31 build 20131206. A graphical front-end for RAxML.
# Created by Daniele Silvestro and Ingo Michalak on 19/05/2010. => dsilvestro@senckenberg.de
# Modified by Madhusudan Gujral on November & December, 2016
try:
    import sys, traceback
    import os  #
    import os.path
    from Tkinter import *
    import Tkinter
    import platform
    import random
    import csv
    import tkMessageBox
    from tkMessageBox import *
    from tkFileDialog import *
    import subprocess
    import commands  ## Added by Madhu
    import time ## Added by Madhu on December 16, 2016
except:
    sys.exit("\nYou need Python 2.5 or higher and the module Tkinter to use raxmlGUI!\n")

# if os.name == 'nt':
# 	proc = subprocess.Popen(["python"], stderr=subprocess.PIPE, shell=True)
# 	(out, err) = proc.communicate()
# 	print "err", err
# 	if "'python' is not recognized" in err:
# 		tkMessageBox.showerror("Python error", "Python is not on the windows path of this machine. Please add python to your path for raxmlGUI to work correctly.")
# 		sys.exit()
# MULTI-PLATFORM
# self_path =os.path.join(os.path.split(__file__)[0]) # is the path of this file
self_path = os.getcwd()  # gives the path of this script if you run it from terminal
# self_path, main = os.path.split(sys.argv[0])
self_path = "%s/raxmlgui" % self_path
# print "Relative script dir: ", self_path
self_path = os.path.abspath(self_path)

PATH_SEP = os.path.sep ## Added by Madhu for testing
test_path = os.path.abspath("%s" % os.path.dirname(os.path.realpath(__file__)))  ## Added by Madhu for testing
print "Test path: " + test_path ## Added by Madhu for testing

global orig_path_dir ## Added by Madhu
orig_path_dir = ""  ## Added by Madhu

import re_tree

##sys.path.insert(0, '%s/python_cipres/' % self_path) ## Commented by Madhu
self_path = os.path.abspath(test_path) ## Added by Madhu for testing
sys.path.insert(0, '%s/python_cipres/' % self_path) ## Added by Madhu for testing

self_path_mod = """ "%s" """ % self_path

raxml_path = os.path.normpath(""" "%s/raxml" """ % self_path)

try:
    import dendropy

    print "loading dendropy library.....done"
except:
    print "dendropy...........Warning: dendropy library not found.\nTo install dendropy follow the instructions after selecting \
the menu option 'Import NEXUS file'. "


def parse_default():
    global K, current_OS, Xterminal
    pref = os.path.normpath("%s/defaults" % self_path) ## Commented by Madhu
    ##pref = os.path.normpath("%s/defaults" % test_path) ## Added by Madhu for testing
    print "Path: " + pref ## Added by Madhu for testing purpose
    pref = file(pref, 'r')
    f = pref.readlines()  # DEFINING PREFERENCES
    K = list()  # R[start:stop:step]
    j = 0

    for i in f:  # defines the preferences
        param = i.split()
        K.insert(j, param[1])  # the second is picked as parameter
        j = j + 1


    ###### Block start added by Madhu ######
    from sys import platform as _platform

    if _platform == "linux" or _platform == "linux2":
         K[6] = "Linux"
    elif _platform == "darwin":
        K[6] = "MacOS"
    elif _platform == "win32":
        K[6] = "Windows"
    ###### Block end added by Madhu ######

    print K ### moved down from before block by Madhu

    current_OS = K[6]
    Xterminal = K[7]

    if K[6] == "MacOS" or K[6] == "Linux":
        K[0] = "./%s" % K[0]


global seed_1, model, outgroup, seed_2, replicate, BSrep, seq_file, exc_file, part_f, outfile, \
    path_dir, status, const_f, fileinputS, dtype, save_brL

seed_1 = model = seed_2 = replicate = exc_file = outfile = numcharC = 0
BSrep = 1
outgroup = exc_file = part_f = status = const_f = ""

###  validateFolder method added by Madhu December 15, 2016
### This is relevant for local run and checks if folder already exists
def validateFolder(fName, selfPath):

    fName = fName.strip()

    if(fName == ""):
        tkMessageBox.showerror("Name problem", "Local run: folder name can't be empty.") ## Added by Madhu
        return False

    if not re.match("^[\w\d_]*$", fName):
        tkMessageBox.showerror("Name problem", "Local run: please provide valid folder name.") ## Added by Madhu
        return False

    newDirectory = selfPath.replace("\"", "").strip() + fName.replace(" ", "_")

    if(os.path.isdir(newDirectory) and cipres_action.get() != 'Run CIPRES-RAxML in background'):
        print "Button 8 value: " + cipres_action.get()
        tkMessageBox.showerror("Name problem", "Local run: folder name already exits, please choose another name.") ## Added by Madhu
        return False

    print "New Directory: " + newDirectory
    return True



# col = "%s" % K[7]# default toolbar color"light Grey" #

def update_menu(status):
    if status == 'open':
        # for i in range(3,8):
        editmenu.entryconfig(3, state=NORMAL)
        editmenu.entryconfig(2, state=DISABLED)
        editmenu.entryconfig(4, state=DISABLED)
        editmenu.entryconfig(5, state=DISABLED)
        # if current_OS=='Windows':
        #	editmenu.entryconfig(2,state=NORMAL)
        #	editmenu.entryconfig(1,state=DISABLED)
        r = [0, 1, 2, 6, 8, 9]
        for i in r: optmenu.entryconfig(i, state=NORMAL)
        # optmenu.entryconfig(3,state=DISABLED)
        # optmenu.entryconfig(4,state=DISABLED)
        mButt3.entryconfig(1, state=NORMAL)
        mButt3.entryconfig(2, state=NORMAL)
        for i in range(0, 4):
            utimenu.entryconfig(i, state=NORMAL)

    if status == 'open_fasta':
        # for i in range(3,8):
        editmenu.entryconfig(2, state=DISABLED)
        editmenu.entryconfig(4, state=DISABLED)
        editmenu.entryconfig(5, state=DISABLED)
        # if current_OS=='Windows':
        #	editmenu.entryconfig(2,state=NORMAL)
        #	editmenu.entryconfig(1,state=DISABLED)
        r = [0, 1, 2, 6, 8, 9]
        for i in r: optmenu.entryconfig(i, state=NORMAL)
        # optmenu.entryconfig(3,state=DISABLED)
        # optmenu.entryconfig(4,state=DISABLED)
        mButt3.entryconfig(1, state=NORMAL)
        mButt3.entryconfig(2, state=NORMAL)
        for i in [0, 2, 3, 4]:
            utimenu.entryconfig(i, state=NORMAL)

    if status == 'clear':
        # for i in range(1,3):
        editmenu.entryconfig(2, state=NORMAL)
        editmenu.entryconfig(3, state=DISABLED)
        editmenu.entryconfig(4, state=NORMAL)
        editmenu.entryconfig(5, state=NORMAL)
        r = [0, 1, 2, 3, 4, 6, 8, 9]
        for i in r: optmenu.entryconfig(i, state=DISABLED)
        # if current_OS=='Windows': optmenu.entryconfig(7,state=DISABLED)
        mButt3.entryconfig(1, state=DISABLED)
        mButt3.entryconfig(2, state=DISABLED)
        for i in range(0, 4):
            utimenu.entryconfig(i, state=DISABLED)

    if status == 'set_part':
        optmenu.entryconfig(2, state=NORMAL)
        optmenu.entryconfig(3, state=NORMAL)
        optmenu.entryconfig(4, state=NORMAL)
        self.bind("<Command-p>", part_short)

    if status == 'del_part':
        optmenu.entryconfig(3, state=DISABLED)
        optmenu.entryconfig(4, state=DISABLED)

    if status == 'pref_on': editmenu.entryconfig(0, state=NORMAL)
    if status == 'pref_off': editmenu.entryconfig(0, state=DISABLED)
    if status == 'exc_on': optmenu.entryconfig(1, state=NORMAL)
    if status == 'exc_off': optmenu.entryconfig(1, state=DISABLED)

    if status == 'part_on':
        optmenu.entryconfig(2, state=NORMAL)
        self.bind("<Command-p>", part_short)
    if status == 'part_off':
        optmenu.entryconfig(2, state=DISABLED)
        self.bind("<Command-p>", nada)


# if status=='constr_on':
#		if current_OS=='Windows': optmenu.entryconfig(4,state=NORMAL)
#		else: optmenu.entryconfig(3,state=NORMAL)
#	if status=='constr_off':
#		if current_OS=='Windows': optmenu.entryconfig(4,state=DISABLED)
#		else: optmenu.entryconfig(3,state=DISABLED)

part_brL = ""


def apply_part_brL():
    global part_brL
    part_brL = askyesno("Per-partition branch lengths", "Use per-partition branch lengths? ", parent=self, default='no')
    print part_brL


def update_bar(status):
    global frame2, f_root
    try:
        frame2.destroy()
        f_root.destroy()
    except:
        pass
    frame2 = Tkinter.Frame(framme, relief=FLAT, borderwidth=1)
    frame2.pack(fill=X, expand=NO, side=LEFT)
    frame2.config(bg=col)
    Label(frame2, text=status, bg=col, fg='dark blue').pack(side=LEFT)


def help_module(v):
    import help
    if v == 1: help.about()
    if v == 2: help.help()
    if v == 3: help.helpraxml()
    if v == 4: help.update()
    if v == 5: help.updateraxml()
    if v == 6: help.joinmail()
    if v >= 7: help.export_citation(v)


def delete():
    global part_f, const_f, part_ff, frame2, dtype, numchar, frame5, II_file, out_list, fileSafe, f_root, fileinputS, numtaxa, rooted_tree
    try:
        numtaxa = 0
    except:
        pass
    try:
        rooted_tree = 0
    except:
        pass
    fileinputS = ""
    texxt.config(state=NORMAL)
    texxt.delete("1.0", END)
    texxt.config(state=DISABLED)
    update_menu('clear')
    try:
        button2.config(highlightbackground=col, text='Load alignment', padx=20, pady=2, command=lambda: open_ali('1'))
    except:
        pass
    out_list = list()
    try:
        del numchar
    except:
        pass
    try:
        frame3.destroy()
    except:
        pass
    try:
        frame4.destroy()
    except:
        pass
    try:
        frame5.destroy()
    except:
        pass
    try:
        frameM.destroy()
    except:
        pass
    try:
        f_constr.destroy()
    except:
        pass
    try:
        del (II_file)
    except:
        pass
    try:
        f_root.destroy()
        button_load_tree.config(highlightbackground=col, text='Load tree file', pady=2, command=add_align)
        rooted_tree = ""
    except:
        pass
    entry.delete("0", END)
    button2.config(state=NORMAL)
    button5.config(state=DISABLED)
    button6.config(state=DISABLED)
    # __ button7.config(state=DISABLED)
    outfile.set('outfile')
    part_ff = part_f = const_f = fileSafe = ""
    ##outfileP = os.path.normpath("%s/part.txt" % self_path) ## Commented by Madhu
    outfileP = os.path.normpath("%s/part.txt" % test_path) ## Added by Madhu
    outfileP = file(outfileP, 'w')
    erase_p = ""
    outfileP.writelines(erase_p)
    raxV = " %s" % K[0]
    update_bar(raxV)
    part_f = ""
    if K[3] == 'rapid' or K[3] == 'thorough':
        def_a = "ML + %s bootstrap" % K[3]
        def_analysis(K[3])
    else:
        def_a = "%s search" % K[3]
    replicate.set(def_a)
    def_analysis(def_a)


def export():
    try:
        global ndata
        frame3.config(bg=col)
        if ndata > 1:
            ans = askyesno("Warning",
                           "By saving and reloading the alignment, the partition settings will be deleted.\n\nDo you want to proceed? ",
                           parent=self)
            if ans:
                svname = asksaveasfilename(title="Save and reload alignment", parent=self)
            else:
                raise
        else:
            svname = asksaveasfilename(title="Save and reload alignment", parent=self)
        if svname:
            global fileinputS, seq_file
            filecontents = texxt.get(1.0, END)
            sv_file = file(svname, 'w')
            sv_file.write(filecontents)
            sv_file.close()
            fileinputS = sv_file
            open_ali(svname)
        else:
            pass
    except:
        pass


def export_part():
    import partition
    partition.export()


def edit():
    showinfo("Notice",
             "To load the new alignment in raxmlGUI after editing, export it from the menu File: Save alignment",
             parent=self)
    texxt.config(state=NORMAL)


def parse_data():
    global model, Imodel, frameM, D, frameMAA, dtype, modelAA, listM, listMAA, Mdtype
    bin = '0' and '1'
    multi = '0' and '2'
    DNA = 'A' and 'T' and 'G' and 'C'
    dna = 'a' and 't' and 'g' and 'c'
    AA = 'F' or 'E' or 'I' or 'L' or 'P' or 'Q' or 'X'
    aa = 'f' or 'e' or 'i' or 'l' or 'p' or 'q' or 'x'
    dtype = StringVar()
    if bin in D and dna in D:
        dtype = "MIXED"
    if bin in D and DNA in D:
        dtype = "MIXED"
    if bin in D and '2' not in D and aa not in D and AA not in D and dna not in D and DNA not in D:
        dtype = "BIN"
    if multi in D and aa not in D and AA not in D and dna not in D and DNA not in D:
        dtype = "MULTI"
    if dna in D and aa not in D and AA not in D and bin not in D and multi not in D:
        dtype = "DNA"
    if DNA in D and aa not in D and AA not in D and bin not in D and multi not in D:
        dtype = "DNA"
    if aa in D and bin not in D:
        dtype = "AA"
    if AA in D and bin not in D:
        dtype = "AA"
    if multi in D:
        Mdtype = "MMulti"
    else:
        Mdtype = " "
    mod_tools()


def mod_tools2():
    try:
        global dtype, dtyp
        dtype = dtyp.get()
        mod_tools()
    except:
        print "No input data file selected!"


def use_F():
    # global model
    m = "%s" % proc.get()
    if '-F' not in m:
        M = "%s -F" % (m)
        proc.set(M)
    else:
        M = m.split()
        proc.set(M[0])


def mod_tools():
    global model, Imodel, frameM, D, frameMAA, dtype, modelAA, listM, modelMU, Mdtype, ndata
    try:
        frameM.destroy()
    except:
        pass
    if replicate.get() == 'Pairwise distances':
        if dtype == "MIXED":
            listM = 'GTRGAMMA', 'GTRGAMMAI', 'BINGAMMA', \
                    'BINGAMMAI', 'MULTIGAMMA', 'MULTIGAMMAI'
            if Mdtype == "MMulti":
                listMMU = 'GTR', 'ORDERED', 'MK'
        if dtype == "BIN":
            listM = 'BINGAMMA', 'BINGAMMAI'
        if dtype == "MULTI":
            listM = 'MULTIGAMMA', 'MULTIGAMMAI'
            listMMU = 'GTR', 'ORDERED', 'MK'
        if dtype == "DNA":
            listM = 'GTRGAMMA', 'GTRGAMMAI',
        if dtype == "AA":
            listM = 'PROTGAMMA', 'PROTGAMMAI',
            listMAA = 'BLOSUM62', 'DAYHOFF', 'DCMUT', 'JTT', 'MTREV', 'WAG', 'RTREV', 'CPREV', 'VT', 'MTMAM', 'LG', 'GTR', 'MTART', 'MTZOA', 'PMB', 'HIVB', 'HIVW', 'JTTDCMUT', 'FLU', 'GTR_UNLINKED'
    else:
        if dtype == "MIXED":
            listM = 'GTRGAMMA', 'GTRGAMMAI', 'GTRCAT', 'GTRCATI', 'GTR', 'GTRI', 'BINGAMMA', \
                    'BINGAMMAI', 'BINCAT', 'BINCATI', 'BIN', 'BINI', 'MULTIGAMMA', 'MULTIGAMMAI', 'MULTICAT', 'MULTICATI', 'MULTI', 'MULTII'
            if Mdtype == "MMulti":
                listMMU = 'GTR', 'ORDERED', 'MK'
        if dtype == "BIN":
            listM = 'BINGAMMA', 'BINGAMMAI', 'BINCAT', 'BINCATI', 'BIN', 'BINI'
        if dtype == "MULTI":
            listM = 'MULTIGAMMA', 'MULTIGAMMAI', 'MULTICAT', 'MULTICATI', 'MULTI', 'MULTII'
            listMMU = 'GTR', 'ORDERED', 'MK'
        if dtype == "DNA":
            listM = 'GTRGAMMA', 'GTRGAMMAI', 'GTRCAT', 'GTRCATI', 'GTR', 'GTRI'
        if dtype == "AA":
            listM = 'PROTGAMMA', 'PROTGAMMAI', 'PROTCAT', 'PROTCATI', 'PROT', 'PROTI'
            listMAA = 'BLOSUM62', 'DAYHOFF', 'DCMUT', 'JTT', 'MTREV', 'WAG', 'RTREV', 'CPREV', 'VT', 'MTMAM', 'LG', 'GTR', 'MTART', 'MTZOA', 'PMB', 'HIVB', 'HIVW', 'JTTDCMUT', 'FLU', 'GTR_UNLINKED'
    frameM = Tkinter.Frame(toolb, relief=FLAT, borderwidth=1)
    frameM.pack(fill=X, expand=NO, side=LEFT)
    frameM.config(bg=col)
    Label(frameM, text=' ', bg=col).pack(side=LEFT)  # DEFINE MODEL
    model = StringVar()
    opt3 = apply(OptionMenu, (frameM, model) + tuple(listM[::1]))
    opt3.pack(side=LEFT)
    opt3.config(bg=col, width=max(len(w) for w in listM) + 3)
    # opt3.pack_propagate(0)
    model.set(listM[0])  # (K[2])
    Imodel = StringVar()
    if dtype == "AA":
        modelAA = StringVar()
        opt1 = apply(OptionMenu, (frameM, modelAA) + tuple(listMAA[::1]))
        opt1.pack(side=LEFT)
        opt1.config(bg=col, width=max(len(w) for w in listMAA) + 3)  # , width =7)
        modelAA.set(listMAA[0])  # (K[2])
        checkM = Checkbutton(frameM, text="Emp. Freq. ", variable=Imodel, onvalue="F", offvalue=" ")
        checkM.pack(side=LEFT)
        checkM.config(bg=col)
        checkM.deselect()
    if dtype == "MULTI" or Mdtype == "MMulti":
        modelMU = StringVar()
        opt1 = apply(OptionMenu, (frameM, modelMU) + tuple(listMMU[::1]))
        opt1.pack(side=LEFT)
        opt1.config(bg=col, width=max(len(w) for w in listMMU) + 3)
        modelMU.set(listMMU[0])  # (K[2])
    try:
        button2.config(highlightbackground=col, text='Add alignment', pady=2, command=add_align)
    except:
        pass
    shortpath = os.path.basename(fileinputS)
    try:
        status = "Sequence file > %s  (%s taxa, %s characters, %s)" % (shortpath, numtaxa, numchar, dtype)
    except(NameError):
        status = "Sequence file > %s  (Fasta file, %s)" % (shortpath, dtype)
    try:
        frame4.config(bg=col)
    except:
        update_bar(status)


def taxa_list(s):
    global frame3, thisline, outg, opt8, shortpath, fileinputS, D, numtaxa, numchar, jstart, M, taxaL, rooted_tree, opt5
    try:
        frame3.destroy()
    except:
        pass
    f = s.readlines()  # DEFINING OUTGROUP
    j = 0
    for j, line in enumerate(f):
        try:
            header = f[j].split()
            numtaxa = int(header[0])
            numchar = header[1]  # print "TAXA", numtaxa, j
            jstart = j
            break
        except:
            pass

    R = list()  # List of taxa
    D = list()  # List of characters
    M = list()
    i = 0
    numtax = numtaxa + 1
    while i < numtax:  # makes the list R (including 1 first line, skipped later)
        taxa = f[i].split()
        if len(taxa) > 1:
            R.insert(i + 1, taxa[0])
        else:
            numtax = numtax + 1
        i = i + 1
    for j, line in enumerate(f):
        m = list()
        if j > jstart:  # skip the header
            dat = line.split()
            if len(dat) > 1:  # when there are 2 items per row (i.e. taxon_name + sequence)
                D.extend(dat[1])  # the second block is taken as "data"
                M.insert(j + 1, dat[1])
            if len(dat) > 0 and len(dat) < 2:
                D.extend(dat[0])
                M.insert(j + 1, dat[0])
    parse_data()
    taxaL = R
    no = "<none>"
    R.insert(1, no)
    if replicate.get() != 'Ancestral states':
        frame3 = Tkinter.Frame(frrr, relief=FLAT, borderwidth=1)
        frame3.pack(fill=X, expand=NO, side=LEFT)
        frame3.config(bg=col)
        Label(frame3, text=" Outgroup", bg=col).pack(side=LEFT)
        outg = StringVar()
        opt8 = apply(OptionMenu, (frame3, outg) + tuple(R[1::1]))  # skip the first item in R (n. taxa)
        opt8.config(bg=col, width=15) ## original width=30 changed by Madhu
        opt8.pack(side=LEFT)
        outg.set(R[1])  # default value is the first taxon
        ##button5.config(state=NORMAL)  # RUN RAXML ## Commented by Madhu 'Change Resource' should enable it
        button6.config(state=NORMAL)  # CLEAR
    # __ button7.config(state=NORMAL)   # RUN CIPRES
    # print "NEWTAXA:", numtaxa, numchar
    elif replicate.get() == 'Ancestral states':
        try:
            if rooted_tree != 0:
                ## button5.config(state=NORMAL) ## Commented by Madhu 'Change Resource' should enable it
                print "Inside Ancestral states" ## Added by Madhu
                # __ button7.config(state=NORMAL)   # RUN RAXML
        except:
            pass
        button6.config(state=NORMAL)  # CLEAR
    if replicate.get() == 'Pairwise distances': opt5.config(state=NORMAL)


def check_seq(arg):
    global seq_file, outfile, frame3, outg, s, seq_f, shortpath, fileinputS, path_dirsimple, mod

    mod = "-m %s" % (model.get())
    if "GAMMA" in model.get() or "CAT" in model.get():
        pass
    else:
        if model.get() in ['PROT', 'GTR', 'MULTI', 'BIN']:
            mod = "-V " + mod + "CAT"
        else:
            if 'PROT' in model.get():
                mod = '-m PROT'
            elif 'GTR' in model.get():
                mod = '-m GTR'
            elif 'MULTI' in model.get():
                mod = '-m MULTI'
            elif 'BIN' in model.get():
                mod = '-m BIN'
            mod = "-V " + mod + "CATI"

    if dtype == "AA":
        if modelAA.get() in ['GTR', 'GTR_UNLINKED'] and Imodel.get() == 'F':
            mod = "%s%s" % (mod, modelAA.get())
        else:
            mod = "%s%s%s" % (mod, modelAA.get(), Imodel.get())

    if dtype == "DNA" or dtype == "MIXED":  # SECONDARY STRUCTURE
        try:
            mod = """%s -S "%s" -A %s""" % (mod, II_file, IIstr.get())
        except:
            pass
    if dtype == "MULTI" or Mdtype == "MMulti":
        mod = "%s -K %s" % (mod, modelMU.get())


    # if dtype == "AA":
    #		mod = "-m %s%s%s" % (model.get(), modelAA.get(), Imodel.get())
    cmd = """cd %s && %s -T 2 -f c %s -s %s -n %s_red -w %s -O""" \
          % (raxml_path, K[0], mod, seq_file, outfile.get(), path_dir)
    print "In check_seq: cmd= ", cmd
    os.system(cmd)
    path_dirsimple = os.path.normpath("%s/" % os.path.dirname(longpath))  # path directory input file
    reduced = """%s%s""" % (fileinputS, ".reduced")
    try:
        red = file(reduced)
        if red and arg == 0:
            print "In check_seq: red= ", red
            ans = askyesno('Warning', """RAxML found at least 1 sequence that is exactly identical \
to other sequences and/or gap-only characters in the alignment.\n\nDo you want to exclude it/them from the analysis?""",
                           parent=self)
            if ans:
                texxt.config(state=NORMAL)
                texxt.delete("1.0", END)
                s = file(reduced, 'r')
                lines = file(reduced, 'r').read()  # lines = s.readlines()
                texxt.insert(END, lines)
                fileinputS = reduced
                seq_file = """ "%s" """ % reduced
                #	frame2.destroy()
                frame3.destroy()
                reduced_file = "%s_red" % outfile.get()
                outfile.set(reduced_file)
                texxt.config(state=DISABLED)
                taxa_list(s)
    except:
        pass


def AAcombi():
    global ndata, button2
    button2.config(state=DISABLED)

    def setAAcombi():
        global dtypeP, ndata
        if data_typeAA.get() in ['GTR', 'GTR_UNLINKED']:
            dtypeP = "%s" % (data_typeAA.get())
        else:
            dtypeP = "%s%s" % (data_typeAA.get(), Imodel.get())
        auto_part()
        button2.config(state=NORMAL)
        AAcomb.destroy()

    AAcomb = Toplevel()
    AAcomb.title("Partition options")
    AAcomb.geometry("280x90")
    AAcomb.minsize(280, 90)
    AAcomb.maxsize(280, 90)
    if current_OS == 'Windows':
        icon = os.path.normpath("%s/icon.ico" % self_path)
        AAcomb.wm_iconbitmap(icon)

    AAcomb.config(bg='light Grey')
    tool = Frame(AAcomb, relief=FLAT, borderwidth=1)
    tool.pack(fill=X, expand=NO, side=TOP)
    tool.config(bg="light Grey")
    t = "substitution model (partition %s):" % (int(ndata) + 1)
    Label(tool, text=t, bg="light Grey").pack(side=TOP)
    toolM = Frame(AAcomb, relief=FLAT)
    toolM.pack(fill=NONE, expand=NO, side=TOP)
    toolM.config(bg="light Grey")
    data_typeAA = StringVar()
    opt4 = OptionMenu(toolM, data_typeAA, 'BLOSUM62', 'DAYHOFF', 'DCMUT', 'JTT', 'MTREV', 'WAG', 'RTREV', 'CPREV', 'VT',
                      'MTMAM', 'LG', 'GTR', 'MTART', 'MTZOA', 'PMB', 'HIVB', 'HIVW', 'JTTDCMUT', 'FLU', 'GTR_UNLINKED')
    opt4.pack(side=LEFT)
    opt4.config(bg="light Grey")  # , width =8)
    data_typeAA.set('BLOSUM62')
    Imodel = StringVar()
    check1 = Checkbutton(toolM, text="Emp. Freq.", variable=Imodel, onvalue="F", offvalue=" ")
    check1.config(bg="light Grey")
    check1.pack(side=LEFT)
    check1.deselect()
    toolN = Frame(AAcomb, relief=FLAT)
    toolN.pack(fill=X, expand=NO, side=BOTTOM)
    toolN.config(bg="light Grey")
    setB = Button(toolN, text='Set', padx=25, pady=2, command=setAAcombi)
    setB.pack(side=TOP)
    setB.config(highlightbackground="light Grey", default=ACTIVE)

    def def_close_setB_short(a):
        setAAcombi()

    AAcomb.bind("<Return>", def_close_setB_short)


def auto_part():
    global dtype, ndata, numcharC, numcharC_1, part_L, com_info, dtypeP, frame2, statusSafe, dtypeSafe
    if ndata == 1:
        if dtype == "AA":
            if modelAA.get() in ['GTR', 'GTR_UNLINKED'] and Imodel.get() == 'F':
                com_info = "%s,	part_1 =	1-%s\n" % (modelAA.get(), numchar)
            else:
                com_info = "%s%s,	part_1 =	1-%s\n" % (modelAA.get(), Imodel.get(), numchar)
        else:
            dtypeP = dtype
            com_info = "%s,	part_%s = %s-%s\n" % (dtypeP, ndata, 1, numchar)
        part_L.insert(0, com_info)
    else:
        com_info = "%s,	part_%s = %s-%s\n" % (dtypeP, ndata, numcharC_1 + 1, numcharC)
        part_L.insert(len(part_L) + 1, com_info)

    combinfo = os.path.normpath("%s/part.txt" % self_path)
    combinfo = file(combinfo, 'w')
    combinfo.writelines(part_L)
    combinfo.close()
    if dtype != dtypeSafe:
        dtype = "MIXED"
        mod_tools()
    shortpath = os.path.basename(fileinputS)
    status = "Sequence file > %scombi.phy  (%s taxa, %s characters, %s partitions)" % (
        shortpath, numtaxa, numcharC, ndata)
    statusSafe = status
    update_bar(status)


def add_align():
    global fileinputS, seq_file, path_dir, s, shortpath, path_d, shortpath, M, numchar, numtaxa, \
        dtype, frame2, jstart, numcharC, ndata, num_taxa, part_L, dtypeP, II_file, fileSafe, statusSafe, dtypeSafe
    try:
        dtypeSafe = dtype
        (fileinputS) = askopenfilename(title="Load new alignment")
        if fileinputS:
            if ndata == 1:
                numcharC = int(numchar)  # print "FIRST", int(numchar), numcharC
                global startJ, numcharC_1
                startJ = int(jstart) + 2.0
                num_taxa = numtaxa
                numcharC_1 = numcharC
                oget = outfile.get()
                comb_file = "%s_comb" % oget
                outfile.set(comb_file)
                auto_part()  # ndata=ndata+1
                update_menu('set_part')
            else:
                startJ = startJ
                numcharC_1 = numcharC  # print "NEW ALIGNMENT"
            try:
                del (II_file)
                frame5.destroy()
                showinfo("Warning", "The secondary structure is ignored with combined data sets!", parent=self)
            except:
                pass

            texxt.config(state=NORMAL)
            texxt.insert(END, "\n")
            s = file(fileinputS, 'U')
            frame3.destroy()
            taxa_list(s)
            # f = s.readlines()  # DEFINING OUTGROUP
            # j=0
            # for j, line in enumerate(f):
            #	try:
            #		header= f[j].split()
            #		numtaxa=int(header[0])
            #		break
            #	except: pass
            if numtaxa != num_taxa:
                showerror("Error", "Wrong number of taxa!")
                raise (SyntaxError)
            combi = os.path.normpath("%s/combi.phy" % self_path)
            combi = file(combi, 'w')
            if dtype == "AA":
                AAcombi()
            for i in range(0, len(M)):
                texxt.insert(END, "\n")
                texxt.insert(END, M[i])
            # print numcharC
            numcharC = numcharC + int(numchar)
            dtypeP = dtype
            texxt.delete("1.0", startJ)
            head = "%s	%s\n" % (num_taxa, numcharC)
            texxt.insert("1.0", head)
            ndata = ndata + 1
            com_data = texxt.get(1.0, END)
            combi.writelines(com_data)
            combi.close()
            numchar = numcharC  # for partitioning
            if dtype != "AA":
                auto_part()
            seq_file = os.path.normpath("%s/combi.phy" % self_path)
            fileSafe = seq_file
            seq_file = """ "%s" """ % seq_file
            fileinputS = os.path.normpath("%s/combi.phy" % self_path)
            #		print "SEQ_NEW_FILE", seq_file
            part_frame()
            texxt.config(state=DISABLED)
    except(SyntaxError):
        #		del_partition()
        fileinputS = fileSafe
        update_bar(statusSafe)
        s = file(fileSafe, 'U')
        taxa_list(s)
    except(NameError):
        pass


def open_ali(open_arg):
    print "In open_ali: open_arg= ", open_arg
    global fileinputS, seq_file, path_dir, s, shortpath, seq_f, path_d, shortpath, ndata, numchar, part_L, fileSafe
    if open_arg == '1' or open_arg == 'self':
        (fileinputS) = askopenfilename(title="Load alignment", parent=self)
    else:
        fileinputS = open_arg
    if fileinputS:
        try:
            s = file(fileinputS, 'U')
            ss = fileinputS
            if open_arg is not '1': delete()
            fileinputS = ss
            fileSafe = fileinputS
            lines = file(fileinputS, 'U').read()  # lines = s.readlines()
            texxt.config(state=NORMAL)
            # for l in range(0,len(lines)): texxt.insert(END, lines[l]) # color lines?
            texxt.insert(END, lines)
            texxt.config(state=DISABLED)
            global seq_file, path_dir, path_dirsimple, longpath
            seq_file = fileinputS
            seq_file = """ "%s" """ % seq_file
            longpath = fileinputS
            shortpath = os.path.basename(longpath)  # name input file
            only_name = os.path.splitext(shortpath)[0]  # file name without extension
            path_dirsimple = os.path.normpath("%s/" % os.path.dirname(longpath))  # path directory input file
            path_dir = os.path.normpath(""" "%s/" """ % os.path.dirname(longpath))  # path directory input file

            outfile.set(only_name)
            taxa_list(s)
            check_seq(0)
            part_L = list()
            ndata = 1
            update_menu("open")
            return 3


            try:
                opt5.config(state=NORMAL)
            except:
                pass
        except:
            showerror("Warning", """File format not supported!\n\nThe alignment file must be in "Phylip" format.""",
                      parent=self)
            delete()


def exc_2():
    try:
        global numchar, ndata, dtype
        frame3.config(bg=col)
        if ndata > 1:
            excyes = askyesno("Warning",
                              "By excluding sites, the partition settings will be deleted. \n\nDo you want to proceed?",
                              parent=self)
            if excyes:
                del_partition()
                exc_3()
            else:
                raise (SyntaxError)
        else:
            exc_3()
    except(SyntaxError):
        pass


def exc_3():
    try:
        if dtype == "MIXED":
            showinfo("Warning", "Site exclusion is not allowed for mixed data sets!", parent=self)
        else:
            outfilenC = os.path.normpath("%s/exc.txt" % self_path)
            outfilenC = file(outfilenC, 'w')
            numcharE = "%s" % numchar
            outfilenC.writelines(numcharE)
            outfilenC.close()
            update_menu('exc_off')
            import exclude
            exclude.exc_start()
    except(NameError, TclError):
        showinfo("Warning", "Please load an alignment first!", parent=self)


def exc():  # copy exclusion file to RAXML directory, run RAXML (saving new dataset in input dir), delete excl file
    global seq_file, frame2, part_f, fileinputS, s, frame3, mod

    try:
        oget = outfile.get()
        frame3.destroy()
        exc_file = os.path.normpath(""" "%s/exc.txt" """ % self_path)
        pro = "-T %s" % proc.get()
        if current_OS == "MacOS" or current_OS == "Linux":
            cmd = """cp %s %s && cd %s && %s %s -f d %s -E exc.txt -s %s -n out -w %s && rm exc.txt""" \
                  % (exc_file, raxml_path, raxml_path, K[0], mod, pro, seq_file, path_dir)
            print "in exc(): cmd= ", cmd
        elif current_OS == "Windows":
            cmd = os.path.normpath(
                """cd %s && xcopy /Y exc.txt %s && cd %s && %s %s -f d %s -E exc.txt -s %s -n out -w %s && del exc.txt""" \
                % (self_path, raxml_path, raxml_path, K[0], mod, pro, seq_file, path_dir))
        os.system(cmd)  # print "COMMAND:", cmd
        #	frame2.destroy()
        entry.delete("0", END)
        fileinputS = """%s.exc.txt""" % (fileinputS)
        seq_file = """ "%s" """ % fileinputS  #
        # print "FILEINPUT_S (after EXC)", fileinputS
        part_f = ""
        red_file = "%s_exc" % oget
        outfile.set(red_file)
        texxt.config(state=NORMAL)
        texxt.delete("1.0", END)
        s = file(fileinputS, 'r')
        lines = file(fileinputS, 'r').read()
        texxt.insert(END, lines)
        texxt.config(state=DISABLED)
        taxa_list(s)
        check_seq(0)
    except NameError:
        showinfo("Warning", "Please load an alignment first!", parent=self)
        # except IOError:
        showerror("Warning", "Bad file format for exclusion site!", parent=self)
        try:
            if current_OS == "MacOS" or current_OS == "Linux":
                cmd = """cd %s && rm -rf %s""" % (raxml_path, shortpathE)
            if current_OS == "Windows":
                cmd = """cd %s && del %s""" % (raxml_path, shortpathE)
            os.system(cmd)
        except:
            pass
        delete()


def constraint(v):
    # frame3.config(bg=col)
    global const_f, replicate, f_constr, taxaL
    try:
        f_constr.destroy()
    except:
        pass
    f_constr = Tkinter.Frame(framme, relief=FLAT, borderwidth=1)
    f_constr.pack(fill=X, expand=NO, side=LEFT)
    f_constr.config(bg=col)
    try:
        if v == '1':
            (fileinput) = askopenfilename(title="Load binary tree")
            if fileinput:
                s = file(fileinput, 'r')
                tree_file = """ "%s" """ % fileinput
                const_f = "-r %s" % tree_file
                shortpathconstr = os.path.basename(tree_file)
                status = "|  Tree constraint > %s" % shortpathconstr
                Label(f_constr, text=status, bg=col, fg='dark blue').pack(side=LEFT)
        if v == '2':
            (fileinput) = askopenfilename(title="Load multifurcating tree")
            if fileinput:
                s = file(fileinput, 'r')
                tree_file = """ "%s" """ % fileinput
                const_f = "-g %s" % tree_file
                shortpathconstr = os.path.basename(tree_file)
                status = "|  Tree constraint > %s" % shortpathconstr
                Label(f_constr, text=status, bg=col, fg='dark blue').pack(side=LEFT)
        if v == '3':
            if replicate.get() == 'ML + rapid bootstrap' and v != '6':
                shift = askyesno("Warning", "The rapid bootstrap will ignore starting trees and constraints.\
 Do you want to keep the starting tree and run a thorough bootstrap analysis instead?", parent=self)
                if shift:
                    def_analysis('ML + thorough bootstrap')
                    replicate.set('ML + thorough bootstrap')
                else:
                    const_f = ""
                    raise

            (fileinput) = askopenfilename(title="Load starting tree")
            if fileinput:
                #		global const_f
                s = file(fileinput, 'r')
                tree_file = """ "%s" """ % fileinput
                const_f = "-t %s" % tree_file
                shortpathconstr = os.path.basename(tree_file)
                shortpath = os.path.basename(fileinputS)
                status = "Sequence file > %s (%s taxa, %s characters) |  Starting tree > %s" % (
                    shortpath, numtaxa, numchar, shortpathconstr)
                update_bar(status)

        if v == '4':
            import constraintM
            constraintM.listTaxa(taxaL, 'constraint')
        if v == '5':
            tree_file = os.path.normpath(""" "%s/constraint.tre" """ % self_path)
            const_f = "-g %s" % tree_file
            shortpath = os.path.basename(fileinputS)
            status = "Sequence file > %s (%s taxa, %s characters) | Tree constrain enforced" % (
                shortpath, numtaxa, numchar)
            update_bar(status)
        if v == '6':
            import constraintM
            constraintM.listTaxa(taxaL, 'out')
    except:
        pass


def del_partition():
    update_menu('del_part')
    global frame4, numchar, frame2, fileinputS, numtaxa, ndata, part_f, part_L
    outfilenC = os.path.normpath("%s/part.txt" % self_path)
    outfilenC = file(outfilenC, 'w')
    erase_p = ""
    outfilenC.writelines(erase_p)
    outfilenC.close()
    frame4.config(bg=col)  # raises an exception when no partition has been defined
    frame4.destroy()
    import partition
    partition.reset_close_main()
    shortpath = os.path.basename(fileinputS)
    status = "Sequence file > %s (%s taxa, %s characters)" % (shortpath, numtaxa, numchar)
    update_bar(status)
    ndata = 1
    part_f = ""
    part_L = list()


def set_partition():
    global part_f, part_brL, part_ff, frame4, numchar, dtype, ndata, frame2, fileinputS, numtaxa
    update_menu('del_part')
    update_menu('part_off')
    part_f = "par"
    outfilenC = os.path.normpath("%s/info.txt" % self_path)
    outfilenC = file(outfilenC, 'w')
    dt = "%s \n%s" % (numchar, dtype)
    outfilenC.writelines(dt)
    outfilenC.close()
    try:
        if ndata > 1:
            import partition
            partition.part_edit()
        else:
            raise
    except:
        try:
            import partition
            partition.part_start()
            part_frame()
            shortpath = os.path.basename(fileinputS)
            status = "Sequence file > %s (%s taxa, %s characters, partitioned)" % (shortpath, numtaxa, numchar)
            update_bar(status)
            ndata = 2
        except:
            raise (NameError)


def part_frame():
    global part_f, part_brL, part_ff, frame4
    try:
        frame4.destroy()
    except:
        pass
    frame4 = Tkinter.Frame(toolb, relief=FLAT, borderwidth=1)
    frame4.pack(fill=X, expand=NO, side=RIGHT)
    frame4.config(bg=col)
    part_brL = StringVar()
    # onn = "-M"
    # check1 = Checkbutton(frame4, text="per-partition brL ", variable=part_brL, onvalue=onn, offvalue=" ")
    # check1.pack(side=RIGHT)
    # check1.config(bg = col)
    # check1.deselect()
    on = os.path.normpath("%s/part.txt" % self_path)
    on = "%s" % on
    part_ff = """-q "%s" """ % (on)


def sec_str():
    try:
        global frame5, IIstr, II_file, dtype, shortpath, numtaxa, numchar, frame2, fileinputS
        if dtype == 'DNA':
            frame3.config(bg=col)
            (fileinput) = askopenfilename(title="Load secondary structure file")
            if fileinput:
                II_file = os.path.abspath(fileinput)
                try:
                    frame5.destroy()
                except:
                    pass
                frame5 = Tkinter.Frame(toolb, relief=FLAT, borderwidth=1)
                frame5.pack(fill=X, expand=NO, side=LEFT)
                frame5.config(bg=col)
                IIstr = StringVar()
                opt4 = OptionMenu(frame5, IIstr, 'S6A', 'S6B', 'S6C', 'S6D', 'S6E', 'S7A', 'S7B', 'S7C', 'S7D', 'S7E',
                                  'S7F', 'S16', 'S16A', 'S16B')
                IIstr.set('S16')
                opt4.pack(side=LEFT)
                opt4.config(bg="light Grey")
                #		frame2.destroy()
                #		frame2 = Tkinter.Frame(framme, relief=FLAT, borderwidth=1)
                #		frame2.pack(fill=X, expand=NO, side=LEFT)
                #		frame2.config(bg=col)
                shortpath = os.path.basename(fileinputS)
                shortpathpart = os.path.basename(II_file)
                status = "Sequence file > %s (%s taxa, %s characters) | Secondary str. > %s" % (
                    shortpath, numtaxa, numchar, shortpathpart)
                update_bar(status)
        # Label(frame2, text=status, bg = col, fg= 'dark blue').pack(side=LEFT)

        else:
            showinfo("Warning", "Data type has to be DNA to use secondary structure.", parent=self)
    except:
        showinfo("No dataset ", "Please load an alignment first!", parent=self)


def consensus(con):
    if con == 'MR': res = 'RAxML_MajorityRuleConsensusTree.'
    if con == 'MRE': res = 'RAxML_MajorityRuleExtendedConsensusTree.'
    if con == 'STRICT': res = 'RAxML_StrictConsensusTree.'
    if con == 'MR_DROP': res, drop_con = 'RAxML_prunedTrees.', 'MR'
    if con == 'STRICT_DROP': res, drop_con = 'RAxML_prunedTrees.', 'STRICT'

    if con == 'RE_conv':
        tree_file = askopenfilename(title="Load tree file")
        if tree_file: re_tree.convert_figtree(tree_file)
    else:
        title = "Load tree file (%s)" % con
        (tree_file) = askopenfilename(title=title)
        if tree_file:
            shortpath = os.path.basename(tree_file)  # name input file
            only_name = os.path.splitext(shortpath)[0]  # file name without extension
            path_dirsimple = os.path.normpath("%s/" % os.path.dirname(tree_file))  # path directory input file
            path_dir = os.path.normpath(""" "%s/" """ % os.path.dirname(tree_file))  # path directory input file

            t_file = tree_file
            t_file = """ "%s" """ % t_file

            if K[5] == "yes":
                result = "%s%s.tre" % (res, only_name)
                if current_OS == 'Windows':
                    result = """ && cd "%s" && start %s" """ % (path_dirsimple, result)
                else:
                    result = """ && cd "%s" && open "%s" """ % (path_dirsimple, result)
            else:
                result = " "
            try:
                remove = "RAxML_info.%s.tre" % (only_name)
                if current_OS == 'Windows':
                    cmd = """cd "%s" && del %s """ % (path_dirsimple, remove)
                else:
                    cmd = """cd "%s" && rm %s """ % (path_dirsimple, remove)
                os.system(cmd)
            except:
                pass
            if con != 'MR_DROP' and con != 'STRICT_DROP':
                msg = """The consensus tree will be saved as:\n "%s%s.tre" """ % (res, only_name)
                showinfo("Run RAxML", msg)
            cmd = """cd %s && %s -T 2 -m GTRGAMMA -z %s -J %s -n %s.tre -w %s %s""" \
                  % (raxml_path, K[0], t_file, con, only_name, path_dir, result)
            print "In consensus(): cmd= ", cmd
            os.system(cmd)
            if con == 'MR_DROP' or con == 'STRICT_DROP':
                pip = """cd %s && %s -T 2 -m GTRGAMMA -z "%s%s%s.tre" -J %s -n %s.Pruned.%s.tre -w %s   """ \
                      % (raxml_path, K[0], path_dirsimple, res, only_name, drop_con, only_name, drop_con, path_dir)
                msg = """The consensus of pruned trees will be saved as:\n "%s%s.Pruned.%s.tre" """ % (
                    res, only_name, drop_con)
                showinfo("Run RAxML", msg)

                os.system(pip)


def Foulds():
    title = "Load tree file for RF distances"
    (tree_file) = askopenfilename(title=title)
    if tree_file:
        shortpath = os.path.basename(tree_file)  # name input file
        only_name = os.path.splitext(shortpath)[0]  # file name without extension
        path_dirsimple = os.path.normpath("%s/" % os.path.dirname(tree_file))  # path directory input file
        path_dir = os.path.normpath(""" "%s/" """ % os.path.dirname(tree_file))  # path directory input file
        t_file = tree_file
        t_file = """ "%s" """ % t_file
        res = "RAxML_RF-Distances"
        msg = """The Robinson Foulds tree distances will be saved as:\n "%s.%sRF.txt" """ % (res, only_name)
        showinfo("Run RAxML", msg)
        cmd = """cd %s && %s -T 2 -m GTRGAMMA -z %s -f r -n %sRF.txt -w %s""" \
              % (raxml_path, K[0], t_file, only_name, path_dir)
        print "In Foulds: cmd= ", cmd
        os.system(cmd)


def CONSEL():
    try:
        frame3.config(bg=col)
        title = "Load tree file for per site log Likelihood"
        (tree_file) = askopenfilename(title=title)
        if tree_file:
            part = ""
            shortpath = os.path.basename(tree_file)  # name input file
            only_name = os.path.splitext(shortpath)[0]  # file name without extension
            path_dirsimple = os.path.normpath("%s/" % os.path.dirname(tree_file))  # path directory input file
            path_dir = os.path.normpath(""" "%s/" """ % os.path.dirname(tree_file))  # path directory input file
            t_file = tree_file
            t_file = """ "%s" """ % t_file
            res = "RAxML_perSiteLLs"
            msg = """The per site log Likelihood will be saved as:\n "%s.%spsL.txt" """ % (res, only_name)
            mod = "-m %s" % (model.get())
            if dtype == "AA":
                if modelAA.get() == 'GTR' and Imodel.get() == 'F':
                    showinfo("Warning",
                             "With amino acid substitution model 'GTR' empirical frequencies cannot be used! Please uncheck the box or choose another substitution model.",
                             parent=self)
                    raise (SyntaxError)
                else:
                    mod = "-m %s%s%s" % (model.get(), modelAA.get(), Imodel.get())
            if dtype == "MIXED":
                if part_f == "":
                    warn = """You need to define partitions to analyze MIXED data sets."""
                    showerror("Warning", warn, parent=self)
                    raise (SyntaxError)
                part = os.path.normpath("-q %s/part.txt" % (self_path))
            showinfo("Run RAxML", msg, parent=self)
            cmd = """cd %s && %s -T 2 %s -s %s -z %s -f g -n %spsL.txt -w %s %s""" \
                  % (raxml_path, K[0], mod, seq_file, t_file, only_name, path_dir, part)
            print "In CONSEL(): cmd= ", cmd
            os.system(cmd)
    except(SyntaxError):
        pass


# except: showinfo("Warning", "Please load an alignment first!", parent=self)

def SH():
    try:
        frame3.config(bg=col)
        title = "Load tree file for SH-like support value computation"
        (tree_file) = askopenfilename(title=title)
        if tree_file:
            part = ""
            mod = "-m %s" % (model.get())
            if dtype == "AA":
                if modelAA.get() == 'GTR' and Imodel.get() == 'F':
                    showinfo("Warning",
                             "With amino acid substitution model 'GTR' empirical frequencies cannot be used! Please uncheck the box or choose another substitution model.",
                             parent=self)
                    raise (SyntaxError)
                else:
                    mod = "-m %s%s%s" % (model.get(), modelAA.get(), Imodel.get())
            if dtype == "MIXED":
                if part_f == "":
                    warn = """You need to define partitions to analyze MIXED data sets."""
                    showerror("Warning", warn, parent=self)
                    raise (SyntaxError)
                part = os.path.normpath("-q %s/part.txt" % (self_path))
            shortpath = os.path.basename(tree_file)  # name input file
            only_name = os.path.splitext(shortpath)[0]  # file name without extension
            path_dirsimple = os.path.normpath("%s/" % os.path.dirname(tree_file))  # path directory input file
            path_dir = os.path.normpath(""" "%s/" """ % os.path.dirname(tree_file))  # path directory input file
            t_file = tree_file
            t_file = """ "%s" """ % t_file
            msg = """The tree with SH values will be saved as:\n "RAxML_fastTreeSH_Support.%s.tre" """ % (only_name)
            showinfo("Run RAxML", msg, parent=self)
            cmd = """cd %s && %s -T 2 %s -s %s -t %s -f J -n %s.tre -w %s %s""" % (
                raxml_path, K[0], mod, seq_file, t_file, only_name, path_dir, part)
            print "In SH(): cmd= ", cmd
            os.system(cmd)
    except(SyntaxError):
        pass


# except: showinfo("Warning", "Please load an alignment first!", parent=self)

def out(outlist):
    global out_list
    out_list = outlist
    outg.set('multiple')


def run(argument):
    global part_f, I_file, IIstr, mod, v_flag
    global path_dir,  orig_path_dir ## This line added by Madhu on Decembet 16, 2016
    v_flag = 0
    check_out = "%s" % outfile.get()
    print check_out
    check_out = check_out.replace(' ', '_')
    outfile.set(check_out)
    inff = os.path.normpath("%s/RAxML_info.%s.tre" % (path_dirsimple, check_out))
    if replicate.get() == 'Ancestral states': inff = os.path.normpath("%s/RAxML_info.%s" % (path_dirsimple, check_out))
    info = "%s" % inff
    print "info: " + info
    try:
        inf = file(info)
        if inf:
            warn = """RAxML output files with the run ID:
                "%s" already exist.\n\nChange output name to run the analysis!""" % outfile.get()
            showerror("Warning", warn, parent=self)

        # elif  BSrep.get() != 'autoMR' and BSrep.get() != 'autoMRE' and BSrep.get() != 'autoMRE_IGN' and BSrep.get() != 'autoFC':
        #		try: int(BSrep.get())
        #		except:
        #			warn="""RAxML output files with the run ID: """
        #			showerror("Warning", warn, parent=self)


    except:
        try:  # DEFINES PARTITIONS IF ANY
            frame4.config(bg=col)  # raises an exception when no partition has been defined
            if part_brL != TRUE and part_brL != FALSE: apply_part_brL()
            if part_brL == TRUE:
                y = "-M"
            else:
                y = " "
            part_f = "%s %s" % (part_ff, y)

        except:
            pass
        try:
            part_f = part_f
        except:
            part_f = ""

        if dtype == "MIXED" and part_f == "":
            warn = """You need to define partitions to analyze MIXED data sets."""
            showerror("Warning", warn, parent=self)
            raise

        o = outg.get()  # define outgroup if any selected
        if o == "<none>":
            o = ""
        elif o == "multiple":
            o = "-o %s" % out_list
        else:
            o = "-o %s" % o

        seed_1 = random.randrange(1, 1000, 1)
        seed_2 = random.randrange(1, 1000, 1)
        global out_file, out_file2, out_file3, result, MLtree, current_OS
        out_file = "%s.tre" % outfile.get()
        out_file1 = "%sR" % outfile.get()
        out_file2 = "%sB" % outfile.get()
        pro = "-T %s" % proc.get()
        # DEFINING THE SUBSTITUTION MODEL
        if "run_CIPRES" in argument:
            try:  # CHECK CIPRES CONFIG FILE
                from os.path import expanduser
                home = expanduser("~")
                conf_file = os.path.normpath("%s/pycipres.conf" % home)
                f = open(conf_file, 'r')
            except(IOError):
                argument = ""
                ans = askyesno("Warning",
                               "No CIPRES config file found, do you want to set it up now? This step is only required once.",
                               parent=self)
                if not ans:
                    return
                conf_CIPRES_ID()

        if "run_CIPRES" in argument:
            def parse_model_inv(model_get):
                global v_flag
                if "GAMMA" not in model_get:
                    if "CAT" not in model_get:
                        v_flag = 1
                        if "I" in model_get[-1]:
                            model_get = model_get[:-1]
                            model_get += "CATI"
                        else:
                            model_get += "CAT"
                if "MULTI" in model_get:
                    model_get = model_get.split("MULTI")[1]
                    add_multi = 1
                else:
                    add_multi = 0
                if "BIN" in model_get:
                    model_get = model_get.split("BIN")[1]
                    add_bin = 1
                else:
                    add_bin = 0
                subs_model = model_get.split("I")[0]
                print "\n\n\n\n\n", "In run(): model_get= ", model_get, "\n\n\n\n\n"

                if model_get.endswith("I"):
                    res = [subs_model, "invariable_=I\n"]
                else:
                    res = [subs_model, ""]
                if add_multi == 1: res[0] = "%s%s" % ("MULTI", res[0])
                if add_bin == 1: res[0] = "%s%s" % ("BIN", res[0])
                return res

            model_get = model.get()
            parsed_model_get = parse_model_inv(model_get)
            print "In run(): parsed_model_get= ", parsed_model_get
            if dtype == "DNA":
                mod = "datatype_=dna\n"  # WHAT ABOUT RNA??
                mod += "dna_gtrcat_=%s\n" % parsed_model_get[0]
            if dtype == "AA":
                mod = "datatype_=protein\n"
                mod += "prot_matrix_spec_=%s\n" % (modelAA.get())
                if Imodel.get() == 'F' and 'GTR' not in modelAA.get():
                    mod += "use_emp_freqs_=T\n"  # check if correct syntax ###editIM: now it is ;)
                else:
                    mod += "use_emp_freqs_=F\n"
                mod += "prot_sub_model_=%s\n" % (parsed_model_get[0])
            if dtype == "MULTI":
                mod = "datatype_=multi\n"
                mod += "multi_model_=%s\n" % parsed_model_get[0]
                mod += "choose_multi_model_=%s\n" % (modelMU.get())
            # HOW DO WE ADD the -K (GTR,ORDERED,MK) OPTION??
            if dtype == "BIN":
                mod = "datatype_=binary\n"
                mod += "bin_model_=%s\n" % parsed_model_get[0]

            # add invariant sites (0/1)
            mod += parsed_model_get[1]

        # other model options:
        #	If not DNA , set datatype_=(protein/rna/binary/multi) then set this parameter
        #	(GTRCAT default;  prot_sub_model_=PROTGAMMA/PROTCAT; rna_model_ ;bin_model_=BINCAT/BINGAMMA; multi_model_=MULTICAT/MULTIGAMMA)
        #	Then set sub_parameters for protein:
        #	prot_matrix_spec_= (DAYHOFF is default)
        #
        #	other modifiers can be set:
        #	invariable_= - switch - Estimate proportion of invariable sites (GTRGAMMA + I)
        #	ascertainment_= switch -
        #	ascertainment_corr_= excl - sets the kind of correction used
        #	use_emp_freqs_= to use empirical frequencies, protein only


        else:

            mod = "-m %s" % (model.get())

            if "GAMMA" in model.get() or "CAT" in model.get():
                pass
            else:
                if model.get() in ['PROT', 'GTR', 'MULTI', 'BIN']:
                    mod = "-V " + mod + "CAT"
                else:
                    if 'PROT' in model.get():
                        mod = '-m PROT'
                    elif 'GTR' in model.get():
                        mod = '-m GTR'
                    elif 'MULTI' in model.get():
                        mod = '-m MULTI'
                    elif 'BIN' in model.get():
                        mod = '-m BIN'
                    mod = "-V " + mod + "CATI"

            if dtype == "AA":
                if modelAA.get() in ['GTR', 'GTR_UNLINKED'] and Imodel.get() == 'F':
                    mod = "%s%s" % (mod, modelAA.get())
                else:
                    mod = "%s%s%s" % (mod, modelAA.get(), Imodel.get())

            if dtype == "DNA" or dtype == "MIXED":  # SECONDARY STRUCTURE
                try:
                    mod = """%s -S "%s" -A %s""" % (mod, II_file, IIstr.get())
                except:
                    pass
            if dtype == "MULTI" or Mdtype == "MMulti":
                mod = "%s -K %s" % (mod, modelMU.get())

        ## Start Block added by Madhu on December 21, 2016
        if(orig_path_dir == ""):
                orig_path_dir = path_dir
            ##else:
            ##    path_dir = orig_path_dir

        if(not validateFolder(outfile.get(), orig_path_dir)):
            return

        path_dir = orig_path_dir.replace("\"","").strip() + outfile.get().strip().replace(" ","_")
        os.system("mkdir " +  path_dir)
        print("Created folder for local run: " + path_dir)

        ## End Block added by Madhu on December 21, 2016


        ## Following line commented by Madhu on December 21, 2016
        ##trees = """ "%s%s%s" """ % (path_dirsimple, "RAxML_bootstrap.", out_file1)
        trees = """ "%s%s%s" """ % (path_dir + PATH_SEP, "RAxML_bootstrap.", out_file1)

        if K[5] == "yes":
            result = "%s%s" % ("RAxML_bipartitions.", out_file)
            # result2 = "%s%s" % ("RAxML_result.", out_file)
            if current_OS == 'Windows':
                result = """ && cd "%s" && start %s """ % (path_dirsimple, result)
            else:
                result = """ && cd "%s" && open "%s" """ % (path_dirsimple, result)

            MLtreeR = """ "%s%s%s" """ % (path_dirsimple, "RAxML_bestTree.", out_file2)
            MLout = """ "%s%s" """ % ("RAxML_bipartitions.", out_file)  # prompts in the info window
            bestTree = "%s%s" % ("RAxML_bestTree.", out_file)
            if current_OS == 'Windows':
                result2 = """ && cd "%s" && start %s """ % (path_dirsimple, bestTree)
            else:
                result2 = """ && cd "%s" && open %s """ % (path_dirsimple, bestTree)

        else:
            result = ""
            result2 = ""
            MLtree = ""
            bestTree = """ "%s%s%s" """ % (path_dirsimple, "RAxML_result.", out_file)
            MLout = """ "%s%s" """ % ("RAxML_bipartitions.", out_file)
            ## Following line replced by Madhu on December 21, 2016
            ##MLtreeR = """ "%s%s%s" """ % (path_dirsimple, "RAxML_bestTree.", out_file2)
            MLtreeR = """ "%s%s%s" """ % (path_dir + PATH_SEP, "RAxML_bestTree.", out_file2)

        if current_OS == 'Windows':
            runWin = "start /wait"
            winD = "/D"
            winEx = "\n exit"
        else:
            runWin = ""
            winD = ""
            winEx = ""

        msg6 = 0
        global rooted_tree

        if "run_CIPRES" in argument:
            if current_OS == 'Windows':
                cp_cmd = "copy"
            else:
                cp_cmd = "cp"
            # create raxml_gui directory
            path_dir_cipres = os.path.normpath("%s/%s/" % (path_dirsimple, "raxmlgui_cipres"))
            os.system("mkdir %s" % path_dir_cipres)

            def get_constraint(s):  # topology, partitions, outgroup
                type_of_constraint = s.split(" ")[0]
                if type_of_constraint in ["-r", "-g", "-q", "-o"]:
                    constr_file = s.split("%s " % (type_of_constraint))[1]
                    constr_file = constr_file.replace('"', '')
                    return [type_of_constraint, constr_file]
                else:
                    return [0, 0]

            def copy_file(file):
                cmd = os.path.normpath("%s %s %s" % (cp_cmd, file, path_dir_cipres))
                os.system(cmd)

            def write_to_file(text_str, file_name):
                file = os.path.normpath("%s/%s" % (path_dir_cipres, file_name))
                newfile = open(file, "w")
                newfile.writelines(text_str)
                newfile.close()

            # prepare testInput.properties and copy input files
            temp = os.path.basename(seq_file)
            input_properties = "infile_=%s\n" % (temp.split('"')[0])
            copy_file(seq_file)

            [set_part, part_file] = get_constraint(part_f)
            if set_part != 0:
                input_properties += "partition_=%s\n" % (os.path.basename(part_file))
                copy_file(part_file)

            [set_constr, constr_file] = get_constraint(const_f)
            if set_constr != 0:
                if set_constr == "-r":
                    input_properties += "binary_backbone_=%s\n" % (os.path.basename(constr_file))
                if set_constr == "-g":
                    input_properties += "constraint_=%s\n" % (os.path.basename(constr_file))
                copy_file(constr_file)
            try:
                valid = re.search('[a-zA-Z]', rooted_tree)
            except:
                valid = 0
            if valid:
                shortpathconstr = os.path.basename(rooted_tree)
                input_properties += "treetop_=%s\n" % (shortpathconstr)

            write_to_file(input_properties, "testInput.properties")

            # __ prepare testParam.properties
            # raxml ID
            if replicate.get() in ["Bootstrap + consensus", "Fast tree search", "ML search", "ML + thorough bootstrap"]:
                raxml_ID = "RAXMLHPC2_WORKFLOW"
            else:  ## ['ML + rapidbootstrap', 'Ancestral states', 'Pairwise distances', 'RELL bootsraps']
                raxml_ID = "RAXMLHPC8_REST_XSEDE"
            param_properties = "toolId=%s\n" % (raxml_ID)

            # add model
            param_properties += mod
            [set_outgroup, outgroup_name] = get_constraint(o)
            if set_outgroup != 0:
                param_properties += "outgroup_=%s\n" % (outgroup_name)

            # __ analysis-specific parameters

            ########## RAXMLHPC8_REST_XSEDE ############

            #### 'ML + rapid bootstrap' ####
            if replicate.get() == 'ML + rapid bootstrap':
                param_properties += "select_analysis_ =fa\n"
                param_properties += "choose_bootstrap_=x\n"
                if save_brL.get() != " ":
                    param_properties += "printbrlength_=1\n"
                else:
                    param_properties += "printbrlength_=0\n"
                if v_flag == 1:
                    param_properties += "disable_ratehet_=1\n"

                try:
                    int(BSrep.get())
                    param_properties += "choose_bootstop_=specify\n"
                    param_properties += "bootstrap_value_=%s\n" % (int(BSrep.get()))  # bootstrap_value_integer

                except(ValueError):  # BOOTSTOPPING
                    param_properties += "choose_bootstop_=bootstop\n"
                    param_properties += "bootstopping_type_=%s\n" % (BSrep.get())

                    # param_properties += "seed_value_=%s\nparsimony_seed_val_=%s" % (seed_1,seed_2) #bootstrap_seed_val_

            elif replicate.get() == 'Pairwise distances':
                param_properties += 'select_analysis_=fx\n'
                if v_flag == 1:
                    param_properties += "disable_ratehet_=1\n"

            elif replicate.get() == 'Ancestral states':
                param_properties += 'select_analysis_=fA\n'
                if v_flag == 1:
                    param_properties += "disable_ratehet_=1\n"

            elif replicate.get() == 'RELL bootstraps':  ## no docs on this yet
                param_properties += 'select_analysis_=fD\n'
                if save_brL.get() != " ":
                    param_properties += "printbrlength_=1\n"
                else:
                    param_properties += "printbrlength_=0\n"
                if v_flag == 1:
                    param_properties += "disable_ratehet_=1\n"

            ######### RAXMLHPC2_WORKFLOW OPTIONS ###########

            ### FAST TREE SEARCH PARAMS ###
            elif replicate.get() == 'Fast tree search':
                param_properties += "specify_workflow_=FTS\n"
                param_properties += "outsuffix_FTS_=infile\n"
                if save_brL.get() == "brl":
                    param_properties += "fasttreesearch_workflow2_=1\n"
                else:
                    param_properties += "fasttreesearch_workflow2_=0\n"
                if BSrep.get() == "sh":
                    param_properties += "fasttreesearch_workflow3_=1\n"
                else:
                    param_properties += "fasttreesearch_workflow3_=0\n"

            ### ML + THOROUGH BOOTSTRAP PARAMS ###
            elif replicate.get() == 'ML + thorough bootstrap':
                param_properties += 'specify_workflow_=MLTB\n'
                param_properties += 'outsuffix_MLTB3_=outfile\n'
                param_properties += 'altrun_number_=%s\n' % BSrep2.get()
                if save_brL.get() != " ":
                    param_properties += "printbrlength_=1\n"
                else:
                    param_properties += "printbrlength_=0\n"

                try:
                    int(BSrep.get())
                    param_properties += "choose_bootstop_=specify\n"
                    param_properties += "bootstrap_value_=%s\n" % (int(BSrep.get()))  # bootstrap_value_integer

                except(ValueError):  # BOOTSTOPPING
                    param_properties += "choose_bootstop_=bootstop\n"
                    param_properties += "bootstopping_type_=%s\n" % (BSrep.get())


            ### ML SEARCH PARAMS ###
            elif replicate.get() == 'ML search':
                param_properties += 'specify_workflow_=MLS\n'
                param_properties += 'outsuffix_MLS_=infile\n'
                param_properties += 'altrun_number_=%s\n' % BSrep2.get()
                if save_brL.get() == "brl":
                    param_properties += "mlsearch_combine_=1\n"
                else:
                    param_properties += "mlsearch_combine_=0\n"
                if BSrep.get() == "sh":
                    param_properties += "mlsearch_shlike_=1\n"
                else:
                    param_properties += "mlsearch_shlike_=0\n"


            ### BOOTSTRAP + CONSENSUS PARAMS ###
            elif replicate.get() == 'Bootstrap + consensus':
                param_properties += 'specify_workflow_=BOOTCON\n'
                param_properties += 'outsuffix_BOOTCON_=boot\n'
                if save_brL.get() != " ":
                    param_properties += "printbrlength_=1\n"
                else:
                    param_properties += "printbrlength_=0\n"

                try:
                    int(BSrep.get())
                    param_properties += "choose_bootstop_=specify\n"
                    param_properties += "bootstrap_value_=%s\n" % (int(BSrep.get()))  # bootstrap_value_integer

                except(ValueError):  # BOOTSTOPPING
                    param_properties += "choose_bootstop_=bootstop\n"
                    param_properties += "bootstopping_type_=%s\n" % (BSrep.get())

            write_to_file(param_properties, "testParam.properties")
            print "\n\ncreated input files in directory: %s\n\n" % (path_dir_cipres)

            print "XXX--O" ## Madhu

            # # GUI for prompting and accepting job names
            ##import python_cipres ## COMMENTED BY Madhu
            try:
                import client as CipresClient ## Added by Madhu in place of previous commented line
                print "client as CipresClient successful"
            except Exception:
                print("\nProblem with previous statement!\n")
                traceback.print_exc(file=sys.stdout)
            ## import client as CipresClient  ## commented by Madhu
            import re
            print "XXX--1" ## Madhu
            properties = CipresClient.Application().getProperties()

            client = CipresClient.Client(properties.APPNAME, properties.APPID, properties.USERNAME, properties.PASSWORD,
                                         properties.URL)
            print "XXX--2" ## Madhu

            try: ## Added by Madhu
                jobs = client.listJobs()
            except Exception: ## Added by Madhu
                print "Rest webservice not accessible." ## Added by Madhu

                import tkMessageBox  ## Added by Madhu
                tkMessageBox.showerror("Webservice problem", "Webservice not accessible, please check your credentials "
                        "in file pycipres.conf in your home directory. If problem is not resolved by fixing credentials "
                        "then please contact Mark Miller. (mmiller@sdsc.edu)") ## Added by Madhu
                sys.exit(1) ## Added by Madhu

            job_name_window = Toplevel(highlightbackground='light Grey')
            job_name_window.title('Job Name')
            ## job_name_window.geometry("520x90") ## commented by Madhu
            job_name_window.geometry("720x60") ## Added by Madhu
            enterJobLabel = Label(job_name_window, text="Enter Job Name:")
            enterJobLabel.pack(side=LEFT)
            v = StringVar()
            global metadata_job_name
            job_entry = Entry(job_name_window, textvariable=v)
            job_entry.pack(side=LEFT)

            def getJobName(jobs):
                if v.get():
                    global metadata_job_name
                    metadata_job_name = v.get()
                    if not re.match("^[\w\d_]*$", metadata_job_name):
                        showinfo("Name format error",
                                 "Please only use a combination of letters, numbers, and underscores.",
                                 parent=job_name_window)
                        return
                    for job in jobs:
                        print "jobName:", job.metadata['clientJobName'], "metadata_job_name:", metadata_job_name
                        if job.metadata['clientJobName'] == metadata_job_name:
                            showinfo("Name error", "That name is already taken. Please choose a different one.",
                                     parent=job_name_window)
                            return
                    job_name_window.destroy()
                else:
                    return

            button_submit = Button(job_name_window, text="Submit", command=lambda: getJobName(jobs))
            ## button_submit.pack(side=LEFT) ## commented by Madhu
            button_submit.pack(side=LEFT, padx = 10, fill=X) ## added by Madhu

            ## Label(job_name_window, text="Would you like an email\n once your job is complete?").pack() ## commented by Madhu
            emailLabel = Label(job_name_window, text="Send me an email when job completes") ## Added by Madhu
            emailLabel.pack(side=LEFT) ## Added by Madhu

            email = IntVar()
            email.set(1) ## Added by Madhu to make sure that "Yes" option is selected by default
            ##Radiobutton(job_name_window, text="Yes", variable=email, value=0).pack(side=RIGHT) ## changed by Mahdu
            Radiobutton(job_name_window, text="Yes", variable=email, value=1).pack(side=LEFT)
            ##Radiobutton(job_name_window, text="No", variable=email, value=1).pack(side=RIGHT) ## chanegd by Madhu
            Radiobutton(job_name_window, text="No", variable=email, value=0).pack(side=LEFT,fill=X)

            global closed_window
            closed_window = 0

            def on_closing():
                job_name_window.destroy()
                global closed_window
                closed_window = 1

            job_name_window.protocol("WM_DELETE_WINDOW", on_closing)
            self.wait_window(job_name_window)
            # END OF Jobname GUI

            #### CHECK THIS LATER
            if argument == 'run_CIPRES' and closed_window != 1:  # try:
                res_dir = os.path.join(path_dirsimple, "%sresults" % outfile.get())
                # cmd= """cd %s %s && python run_cipres_lib.py -d %s -wd %s %s""" % (winD, self_path,path_dir_cipres,res_dir,winEx)
                # print "In run(): cmd= ", cmd
                metadata_job_name = metadata_job_name.strip().replace(" ", "_")
                print "winEx:", winEx
                cmd = """cd %s %s && python run_cipres_lib.py -d %s -wd %s -n %s -m %s""" % (
                    winD, self_path, path_dir_cipres, metadata_job_name, metadata_job_name, email.get())
                print "In run(): cmd= ", cmd

            if argument == 'run_CIPRES_background' and closed_window != 1:
                res_dir = os.path.join(path_dirsimple, "%sresults" % outfile.get())
                cmd = """cd %s %s && python run_cipres_lib_bg.py -d %s -wd %s -n %s""" % (
                    winD, self_path, path_dir_cipres, res_dir, metadata_job_name)
                print "In run(): cmd= ", cmd

                #### Block added by Madhu start ####
                try:
                    print "Before Returned: "

                    if current_OS == 'Windows':
                        returnedVal = subprocess.check_output(cmd, shell=True)
                        ## commands.getoutput(cmd) .. etc. does not work on Windows
                    else:
                        returnedVal = commands.getoutput(cmd)

                    ## print "Returned: " + returnedVal
                    if("HTTP Code: 400, Form validation error" in returnedVal): ## Added by Madhu
                        import tkMessageBox  ## Added by Madhu
                        tkMessageBox.showerror("Problem with choosing parameter", returnedVal) ## Added by Madhu
                        sys.exit(1) ## Added by Madhu

                except Exception:
                    print "Caught error!!"
                    sys.exit(1)

                #### Block added by Madhu end ####

                ##os.system(cmd) commented by Madhu

                showinfo("raxmlGUI-CIPRES analysis", "Your analysis was submitted to the CIPRES servers."
                    "You will be notified by email when the analysis is done.\n\nYou can check the status"
                    " of your runs and download the results to a folder of your choice by selecting 'Use CIPRES > Check CIPRES Jobs'.")

        ####### RUN RAXML LOCALLY #######
        else:
            ## Block added by Madhu (Start) on December 16, 2016 that creates new folder defined in outfile field.
            ## In addition, the 'path_dir' is updated for local use so that the in 'cmd' is 'path_dir' the correct path.
            """
            if(orig_path_dir == ""):
                orig_path_dir = path_dir
            ##else:
            ##    path_dir = orig_path_dir

            if(not validateFolder(outfile.get(), orig_path_dir)):
                return

            path_dir = orig_path_dir.replace("\"","").strip() + outfile.get().strip().replace(" ","_")
            os.system("mkdir " +  path_dir)
            print("Created folder for local run: " + path_dir)
            """
            ## Block added by Madhu (End) on December 16, 2016

            if replicate.get() == 'Ancestral states':
                msg6 = 1
                out_file = "%s" % outfile.get()
                cmd = """cd %s %s && %s %s -f A -t "%s" -s %s %s -n %s -O -w %s %s %s""" \
                      % (winD, raxml_path, K[0], pro, rooted_tree, seq_file, mod, out_file, path_dir, part_f, winEx)

            if replicate.get() == 'Pairwise distances':
                # "./raxmlHPC -f x -m GTRGAMMA[I] -n NAME -s INPUT -p RANDOMNR [-q PARTFILE -o OUTGROUP]"
                cmd = """cd %s %s && %s %s -f x -p %s %s -s %s %s -n %s %s -O -w %s %s %s""" \
                      % (
                          winD, raxml_path, K[0], pro, seed_1, const_f, seq_file, mod, out_file, o, path_dir, part_f,
                          winEx)

            if replicate.get() == 'RELL bootstraps':
                # "./raxmlHPC -f x -m GTRGAMMA[I] -n NAME -s INPUT -p RANDOMNR [-q PARTFILE -o OUTGROUP]"
                cmd = """cd %s %s && %s %s -f D -p %s %s -s %s %s -n %s %s -O -w %s %s %s""" \
                      % (
                          winD, raxml_path, K[0], pro, seed_1, const_f, seq_file, mod, out_file, o, path_dir, part_f,
                          winEx)

            if replicate.get() == 'ML + rapid bootstrap':  ### rapid BS ###
                cmd = """cd %s %s && %s %s %s -f a -x %s %s %s -p %s -N %s %s -s %s -n %s %s -O -w %s %s %s %s""" \
                      % (winD, raxml_path, runWin, K[0], pro, seed_1, save_brL.get(), mod, seed_2, BSrep.get(), o,
                         seq_file, out_file, part_f, path_dir, const_f, result, winEx)

            elif replicate.get() == 'ML + thorough bootstrap':  ### throrough BS ###
                cmd = """cd %s %s \
	                && %s %s -b %s %s %s -p %s -N %s %s -s %s -n %s %s -w %s %s -O && cd %s \
	                && %s %s -f d %s %s -s %s -N %s -n %s %s -w %s %s -p %s -O && cd %s \
	                && %s %s -f b -t %s -z %s %s -s %s -n %s -w %s %s -O %s""" \
                      % (winD, raxml_path, K[0], pro, seed_1, mod, save_brL.get(), seed_2, BSrep.get(), o, seq_file,
                         out_file1, part_f, path_dir, const_f,
                         raxml_path, K[0], pro, mod, o, seq_file, BSrep2.get(), out_file2, part_f, path_dir, const_f,
                         random.randrange(1, 1000, 1),
                         raxml_path, K[0], pro, MLtreeR, trees, mod, seq_file, out_file, path_dir, result, winEx)

                try:
                    remove = "RAxML_info.%s.tre" % (only_name)
                    if current_OS == 'Windows':
                        cmd = """cd "%s" && del %s """ % (path_dirsimple, remove)
                    else:
                        cmd = """cd "%s" && rm %s """ % (path_dirsimple, remove)

                    ## os.system(cmd)  ## commented by Madhu and replaced by following line
                    ## os.system(cmd) or commands.getoutput(cmd) do not work on Windows environment
                    returnedValue = subprocess.check_output(cmd, shell=True)
                    print "Running RAxML locally: " + returnedValue

                except:
                    pass

            elif replicate.get() == 'Bootstrap + consensus':  ### only BS ###
                msg6 = 2
                if current_OS == 'Windows':
                    remove_cmd = "del"
                else:
                    remove_cmd = "rm"

                ## Following line replaced by Madhu and replaced by subsequent line on December 21, 2016
                ##BStrees_file = """  "%sRAxML_bootstrap.%s"    """ % (path_dirsimple, out_file) ## Commented by  Madhu
                BStrees_file = """  "%sRAxML_bootstrap.%s"    """ % (path_dir + PATH_SEP, out_file)
                cmd = """cd %s %s \
	                && %s %s %s %s -n %s -s %s %s -x %s -N %s -w %s %s %s -p %s -O && cd %s\
	                && %s %s %s -n con.%s -J MR -z %s -w %s %s""" \
                      % (winD, raxml_path, \
                         K[0], pro, mod, save_brL.get(), out_file, seq_file, o, seed_1, BSrep.get(), path_dir, part_f,
                         const_f, random.randrange(1, 1000, 1), raxml_path, \
                         K[0], pro, mod, out_file, BStrees_file, path_dir, winEx)


            elif replicate.get() == 'ML search':  ### only ML search ###
                # calculate SH
                if BSrep.get() == "sh":
                    ## Following line replaced by Madhu and replaced by subsequent line on December 21, 2016
                    ##intreefile2 = """ "%s%s%s" """ % (path_dirsimple, "RAxML_bestTree.", out_file)
                    intreefile2 = """ "%s%s%s" """ % (path_dir + PATH_SEP, "RAxML_bestTree.", out_file)

                    ## Following line replaced by Madhu and replaced by subsequent line on December 21, 2016
                    ##cmd_temp2 = """ && cd %s %s && %s %s -f J %s -t %s -n sh.%s -s %s -w %s %s -O""" \
                    cmd_temp2 = """ && cd %s %s && %s %s -f J %s -t %s -n RAxML_info.%s -s %s -p %s -w %s %s -O""" \
                                % (winD, raxml_path, K[0], pro, mod, intreefile2, out_file, seq_file, random.randrange(1, 1000, 1), path_dir, part_f)
                    ## Following line changed by Madhu on December 22, 2016
                    ##MLout = "RAxML_bestTree.sh." + out_file
                    MLout = "RAxML_bestTree." + out_file
                else:
                    cmd_temp2 = ""
                    MLout = "RAxML_bestTree." + out_file
                # && cd /D USERSFOLDER && type RAxML_result.INPUTNAME* > combinedresults.INPUTNAME.trees
                # && cd USERSFOLDER && cat RAxML_result.INPUTNAME* > combinedresults.INPUTNAME.trees
                if save_brL.get() == "brl":
                    if current_OS == 'Windows':
                        combine_trees = os.path.normpath(
                            " && cd /D %s && type RAxML_result.%s* > combined_results.%s" % (
                                path_dir, out_file, out_file))
                    else:
                        combine_trees = " && cd %s && cat RAxML_result.%s* > combined_results.%s" % (
                            path_dir, out_file, out_file)
                    MLout = "combined_results." + out_file
                else:
                    combine_trees = ""

                MLtree = "%s%s%s" % (path_dir, "RAxML_result.", out_file)
                cmd = """cd %s %s && %s %s -f d %s -N %s -O -p %s %s -s %s -n %s %s -w %s %s %s %s %s %s""" \
                      % (winD, raxml_path, K[0], pro, mod, BSrep2.get(), random.randrange(1, 1000, 1), o, seq_file,
                         out_file, part_f, path_dir, const_f, result2, cmd_temp2, combine_trees, winEx)

            elif replicate.get() == 'Fast tree search':  ### fast Tree search ###
                # calculate brL
                if save_brL.get() == "brl":
                    msg6 = 4
                    ## Following line replaced by Madhu and replaced by subsequent line on December 21, 2016
                    ##intreefile1 = """ "%s%s%s" """ % (path_dirsimple, "RAxML_fastTree.", out_file)
                    intreefile1 = """ "%s%s%s" """ % (path_dir +  PATH_SEP, "RAxML_fastTree.", out_file)
                    cmd_temp1 = """ && cd %s %s && %s %s -f e %s -t %s -n brL.%s -s %s -w %s %s -O""" \
                                % (winD, raxml_path, K[0], pro, mod, intreefile1, out_file, seq_file, path_dir, part_f)
                else:
                    cmd_temp1 = ""

                # calculate SH
                if BSrep.get() == "sh":
                    if save_brL.get() == "brl":
                        ## Following line replaced by Madhu and replaced by subsequent line on December 21, 2016
                        ##intreefile2 = """ "%s%s%s" """ % (path_dirsimple, "RAxML_result.brL.", out_file)
                        intreefile2 = """ "%s%s%s" """ % (path_dir + PATH_SEP, "RAxML_result.brL.", out_file)
                    else:
                        ## Following line replaced by Madhu and replaced by subsequent line on December 21, 2016
                        ##intreefile2 = """ "%s%s%s" """ % (path_dirsimple, "RAxML_fastTree.", out_file)
                        intreefile2 = """ "%s%s%s" """ % (path_dir + PATH_SEP, "RAxML_fastTree.", out_file)
                    ##cmd_temp2 = """ && cd %s %s && %s %s -f J %s -t %s -n sh.%s -s %s -w %s %s -O""" \
                    cmd_temp2 = """ && cd %s %s && %s %s -f J %s -t %s -n sh.%s -s %s  -p %s -w %s %s -O""" \
                                % (winD, raxml_path, K[0], pro, mod, intreefile2, out_file, seq_file, random.randrange(1, 1000, 1), path_dir, part_f)
                    msg6 = 3
                else:
                    cmd_temp2 = ""

                if cmd_temp1 == "" and cmd_temp2 == "": msg6 = 5

                cmd = """cd %s %s && %s %s -f E -p %s %s -n %s -s %s -O -w %s %s %s %s %s""" \
                      % (winD, raxml_path, K[0], pro, seed_1, mod, out_file, seq_file, path_dir, part_f, cmd_temp1,
                         cmd_temp2, winEx)

            ##path_dir = orig_path_dir ## Added by Madhu on December 16, 2016 so that path_dir varoiable is set to
            ## original value once the local run completes.

            ##print "THIS IS A CHECK, Path_dir reset to the original value: " + path_dir ## Added by Madhu on December 16,2016


        if argument == 'e':  # showinfo("RAxML command", cmd) #, parent=self)
            def export_cmd():
                svname = asksaveasfilename(title="Save RAxML command")
                if svname:
                    filecontents = texxt_1.get(1.0, END)
                    sv_file = file(svname, 'w')
                    sv_file.write(filecontents)

            self_1 = Toplevel()
            self_1.title("Inspect RAxML command")
            self_1.geometry("565x230")
            self_1.minsize(565, 230)
            self_1.config(bg='light Grey')
            self_1.grab_set()
            if current_OS == 'Windows':
                icon = os.path.normpath("%s/icon.ico" % self_path)
                self_1.wm_iconbitmap(icon)
            b = Frame(self_1, relief=RAISED, borderwidth=1)
            b.pack(fill=X, expand=NO, side=BOTTOM)
            b.config(bg="light Grey")
            Label(b, text='  ', bg="light Grey").pack(side=RIGHT)
            setA = Button(b, text='Close', padx=25, pady=2, command=self_1.destroy)
            setA.pack(side=RIGHT)
            setA.config(highlightbackground="light Grey")
            setB = Button(b, text='Save to file', padx=25, pady=2, command=export_cmd)
            setB.pack(side=RIGHT)
            setB.config(highlightbackground="light Grey")
            texxt_1 = Text(self_1, padx=35, pady=0, width=20, height=10)
            texxt_1.pack(side=TOP, expand=NO)  # , fill=Y)
            texxt_1.config(highlightthickness=0)
            sbar = Scrollbar(self_1)
            sbar.config(command=texxt_1.yview)
            texxt_1.config(yscrollcommand=sbar.set)
            sbar.pack(fill=Y, expand=YES)
            if current_OS == 'MacOS' or current_OS == 'Windows':
                texxt_1.config(relief=GROOVE, bg='#e6e6e6', fg='dark blue', font=(11), state=DISABLED)
            else:
                texxt_1.config(relief=GROOVE, bg='#e6e6e6', fg='dark blue', font=('Monaco', 10), state=DISABLED)
            texxt_1.pack(side=LEFT, expand=YES, fill=BOTH)
            texxt_1.config(state=NORMAL)
            texxt_1.insert(END, cmd)
            texxt_1.config(state=DISABLED)

            def close_cmd(a):
                self_1.destroy()

            self_1.bind("<Escape>", close_cmd)
            self_1.bind("<Command-w>", close_cmd)
            if current_OS == 'Windows': self_1.bind("<Control-w>", close_cmd)

        closed_window = 0 ## Added by Madhu
        if (argument == "r" or argument == "run_CIPRES") and closed_window != 1:

            if current_OS == 'MacOS' or current_OS == 'Linux':

                try:
                    try:
                        if current_OS == 'MacOS' and Xterminal == 'Terminal':
                            check_path = self_path.split()
                            if len(check_path) > 1:
                                raise
                            cmdfile = os.path.normpath("%s/cmdMac" % self_path)
                            cmdfile = file(cmdfile, 'w')
                            cmdfile.writelines(cmd)
                            cmdfile.close()
                            cmdScript = os.path.normpath(
                                """osascript -e 'tell application "Terminal" to do script "%s/cmdMac" '""" % self_path)

                            print "In run(): cmdScript= ", cmdScript
                            os.system(cmdScript)
                        else:
                            raise
                    except:
                        cmdMac = """xterm -e '%s' & """ % cmd
                        print "\n\n", "In run(): cmdMac= ", cmdMac, "\n\n"
                        os.system(cmdMac)
                except:
                    os.system(cmd)
            if current_OS == 'Windows' and closed_window != 1:
                try:
                    cmdfile = os.path.normpath("%s/cmdWin.bat" % self_path)
                    cmdfile = file(cmdfile, 'w')
                    cmdfile.writelines(cmd.replace("\"", "", 10))
                    cmdfile.close()
                    ##cmdScript = os.path.normpath(""" start "" "%s/cmdWin.bat" """ % self_path) ## Changed by Madhu
                    cmdScript = os.path.normpath("""start  %s/cmdWin.bat """ % self_path) ## Added by Madhu
                    os.system(cmdScript)
                    ##retVal = subprocess.check_output(cmdScript, shell=True) ## Added by Madhu then commented
                except:
                    ## os.system(cmd) ## Commented by Madhu and replaced by following line
                    os.system(cmd.replace("\"", "", 10)) ## Added by Madhu

        ## On December 16, 2016, following three lined were added by Madhu to disable local run button for 15 seconds,
        ## upon the job launch but I decided to remove it because it creates confusion. 15 seconds completion does not
        # mean the job is completed. Techinically job run may take less than 15 seconds or way more than 15 seconds.
        ##button8.config(state=DISABLED)
        ##time.sleep(15)
        ##button8.config(state=NORMAL)

        msg5 = """The result will be saved as %s """ % MLout
        if msg6 == 1: msg5 = """The results will be saved in %s """ % path_dir
        if msg6 == 2: msg5 = """The result will be saved as "RAxML_MajorityRuleConsensusTree.con.%s" """ % out_file
        if msg6 == 3: msg5 = """The result will be saved as "RAxML_fastTreeSH_Support.sh.%s" """ % out_file  # brl + SH
        if msg6 == 4: msg5 = """The result will be saved as "RAxML_result.brl.%s" """ % out_file  # brl
        if msg6 == 5: msg5 = """The result will be saved as "RAxML_fastTree.%s" """ % out_file
        infofile = """ "%s%s%s" """ % (path_dirsimple, "RAxML_info.", out_file)
        msg1 = "running RAxML...", msg5
        msg1 = list(msg1)

        if argument == "r":
            update_bar(msg1[0])
            self.after(1000, lambda: update_bar(msg1[1]))

        path_dir = orig_path_dir ## Added by Madhu on December 21, 2016 so that path_dir varoiable is set to
        ## original value once the local run completes.

        print "THIS IS A CHECK, Path_dir reset to the original value: " + path_dir ## Added by Madhu on December 21,2016

def set():
    update_menu('pref_off')
    import pref
    pref.find()


def open_rooted_tree():
    global rooted_tree, f_root, numtaxa
    rooted_tree = askopenfilename(title="Load rooted tree")
    print "In open_rooted_tree(): rooted tree= ", rooted_tree
    if rooted_tree:
        try:
            f_root.destroy()
        except:
            pass
        button6.config(state=NORMAL)
        if numtaxa:
            if numtaxa > 0:
                print "In open_rooted_tree(): numtaxa= ", numtaxa
                ##button5.config(state=NORMAL) ## Commented by Madhu 'Change Resource' should enable it
                # __ button7.config(state=NORMAL)
        shortpathconstr = os.path.basename(rooted_tree)
        f_root = Tkinter.Frame(framme, relief=FLAT, borderwidth=1)
        f_root.pack(fill=X, expand=NO, side=LEFT)
        f_root.config(bg=col)
        status = "| Tree file > %s" % shortpathconstr
        Label(f_root, text=status, bg=col, fg='dark blue').pack(side=LEFT)
        try:
            button_load_tree.config(highlightbackground=col, text='Change tree file', pady=2, command=open_rooted_tree)
        except:
            pass


def import_fasta():
    global fileinputS, seq_file, path_dir, s, shortpath, seq_f, path_d, shortpath, ndata, numchar, part_L, fileSafe, dtype
    global frame3, thisline, outg, opt8, shortpath, fileinputS, D, numtaxa, numchar, jstart, M, taxaL, rooted_tree, opt5, Mdtype
    global only_name  ## Added by Madhu

    try:
        import dendropy
        try:
            fileinput = askopenfilename(title="Select FASTA matrix")
            if fileinput:
                if 2 > 1:  # try:
                    print "In import_fasta(): fileinput= ", fileinput
                    taxa = dendropy.TaxonSet()
                    try:
                        Matrix = dendropy.DnaCharacterMatrix.get_from_path(fileinput, 'fasta',
                                                                           preserve_underscores=True,
                                                                           data_type='protein', taxon_set=taxa)
                        dtype = "AA"
                    except:
                        try:
                            Matrix = dendropy.DnaCharacterMatrix.get_from_path(fileinput, 'fasta',
                                                                               preserve_underscores=True,
                                                                               data_type='dna', taxon_set=taxa)
                            dtype = "DNA"
                        except(dendropy.utility.error.DataParseError):
                            delete()
                            showerror("Warning", """File format not recognized""", parent=self)

                    list_t = list()
                    for t in taxa: list_t.append(str(t).split()[0])

                    fileinputS = fileinput

                    s = file(fileinputS, 'U')
                    ss = fileinputS
                    lines = file(fileinputS, 'U').read()  # lines = s.readlines()
                    texxt.config(state=NORMAL)
                    texxt.insert(END, lines)
                    texxt.config(state=DISABLED)
                    global seq_file, path_dir, path_dirsimple, longpath
                    seq_file = fileinputS
                    seq_file = """ "%s" """ % seq_file
                    longpath = fileinputS
                    shortpath = os.path.basename(longpath)  # name input file
                    only_name = os.path.splitext(shortpath)[0]  # file name without extension
                    path_dirsimple = os.path.normpath("%s/" % os.path.dirname(longpath))  # path directory input file
                    path_dir = os.path.normpath(""" "%s/" """ % os.path.dirname(longpath))  # path directory input file
                    outfile.set(only_name)


                    # taxa_list(s)


                    try:
                        frame3.destroy()
                    except:
                        pass

                    w = Matrix.as_string("fasta")
                    w = w.split('>')
                    WW = w[1].split()
                    # WW=W.split()

                    numchar = len(WW[len(WW) - 1])
                    numtaxa = len(list_t)

                    taxaL = list_t
                    R = list_t
                    no = "<none>"
                    R.insert(1, no)
                    if replicate.get() != 'Ancestral states':
                        frame3 = Tkinter.Frame(frrr, relief=FLAT, borderwidth=1)
                        frame3.pack(fill=X, expand=NO, side=LEFT)
                        frame3.config(bg=col)
                        Label(frame3, text=" Outgroup", bg=col).pack(side=LEFT)
                        outg = StringVar()
                        opt8 = apply(OptionMenu, (frame3, outg) + tuple(R[1::1]))  # skip the first item in R (n. taxa)
                        opt8.config(bg=col, width=30)
                        opt8.pack(side=LEFT)
                        outg.set(R[1])  # default value is the first taxon
                        ##button5.config(state=NORMAL)  # RUN RAXML## Commented by Madhu 'Change Resource' should enable it
                        button6.config(state=NORMAL)  # CLEAR
                    # __ button7.config(state=NORMAL)
                    # print "NEWTAXA:", numtaxa, numchar
                    elif replicate.get() == 'Ancestral states':
                        try:
                            if rooted_tree != 0:
                                ##button5.config(state=NORMAL) ## Commented by Madhu 'Change Resource' should enable it
                                print "Inside Ancestral states" ## Added by Madhu
                                # __ button7.config(state=NORMAL)
                        except:
                            pass
                        button6.config(state=NORMAL)  # CLEAR
                    if replicate.get() == 'Pairwise distances': opt5.config(state=NORMAL)
                    Mdtype = " "
                    mod_tools()
                    button2.config(state=DISABLED)

                    check_seq(0)
                    part_L = list()
                    ndata = 1
                    update_menu("open_fasta")
                    # update_menu("open")

                    try:
                        opt5.config(state=NORMAL)
                    except:
                        pass

        except:
            pass

    except(ImportError):
        install_dendropy()
    except:
        pass


def convert_matrix(arg):
    try:
        import dendropy
        if arg == 'nex2phy':
            fileinput = askopenfilename(title="Select NEXUS matrix")
            if fileinput:
                try:
                    print "In convert_matrix(): fileinput=", fileinput
                    nex = dendropy.DataSet.get_from_path(fileinput, 'nexus', preserve_underscores=True,
                                                         suppress_annotations=True)
                    # print nex
                    svname = asksaveasfilename(title="Save as Phylip file")  # , parent=self)
                    if svname:
                        nex.write_to_path(svname, 'phylip', preserve_underscores=True)
                        # ans=askyesno("Load alignment", "Open new Phylip alignment? ", parent=self, default='yes')
                        # if ans:
                        open_ali(svname)
                except(dendropy.utility.error.DataParseError):
                    showerror("Warning", """File format not recognized""", parent=self)
                except:
                    showerror("Warning", """File format not recognized""", parent=self)
        if arg == 'phy2nex':
            try:
                global ndata, dtype
                print "In convert_matrix(): dtype=", dtype
                if dtype == 'DNA':
                    dtypeN = 'dna'
                elif dtype == 'AA':
                    dtypeN = 'protein'
                else:
                    dtypeN = 'standard'
                frame3.config(bg=col)
                svname = asksaveasfilename(title="Save and export alignment", parent=self)
                if svname:
                    filecontents = texxt.get(1.0, END)
                    sv_file = file(svname, 'w')
                    sv_file.write(filecontents)
                    sv_file.close()
                    print "In convert_matrix(): dtypeN=", dtypeN
                    try:
                        ali = dendropy.DataSet.get_from_path(svname, 'phylip', data_type=dtypeN,
                                                             preserve_underscores=True, interleaved=True)
                    except:
                        ali = dendropy.DataSet.get_from_path(svname, 'fasta', data_type=dtypeN,
                                                             preserve_underscores=True, interleaved=True)
                    ali.write_to_path(svname, 'nexus', data_type=dtypeN, preserve_underscores=True, simple=True,
                                      unquoted_underscores=True)
                else:
                    pass
            except:
                pass

    except(ImportError):
        install_dendropy()


def restart_me():
    if current_OS == 'Windows':
        s = self_path
        s += "____"
        self_path_root = s.replace('raxmlgui____', '')
        print s, self_path_root
        cmdScript = os.path.normpath(""" start "raxmlGUI console" /D "%s" raxmlGUI.py""" % self_path_root)

    elif current_OS == 'MacOS':
        cmdScript = """osascript -e 'tell application "Terminal" to do script "cd '%s' && cd .. && python raxmlGUI.py > output.txt" '""" % self_path
    else:
        cmdScript = """xterm -e 'cd "%s" && cd .. && python raxmlGUI.py ' & """ % self_path
    print "In restart_me(): cmdScript=", cmdScript
    os.system(cmdScript)
    self.quit()


def install_dendropy():
    def select_dendropy_dir():
        dir = dendro_path = askdirectory(title="Select uncompressed dendropy folder")  # , parent=self)
        if dir:
            print "In install_dendropy(): dendro_path=", dendro_path
            if current_OS == 'Windows':
                dendro_path = os.path.normpath(dendro_path.replace('/', '\\'))
                print "In install_dendropy(): dendro_path=", dendro_path
                cmd = os.path.normpath("""cd /D "%s" && %s setup.py install""" % (dendro_path, sys.executable))
            else:
                cmd = """cd "%s" && python setup.py install""" % (dendro_path)
            print "In install_dendropy(): cmd=", cmd

            os.system(cmd)
            ans = askyesno("dendropy", "You must restart raxmlGUI to make the changes effective. Restart now?",
                           parent=self)
            if ans: restart_me()

    ans = askyesno("Library dendropy required", """This function requires the Python library 'dendropy'.
Do you want to download and install 'dendropy' now?""", parent=self)
    if ans:
        if current_OS == 'MacOS':
            cmd = "open https://github.com/jeetsukumaran/DendroPy/zipball/master"
            os.system(cmd)
        if current_OS == 'Linux':
            cmd = "xdg-open https://github.com/jeetsukumaran/DendroPy/zipball/master"
            os.system(cmd)
        if current_OS == 'Windows':
            cmd = os.path.normpath("start https://github.com/jeetsukumaran/DendroPy/zipball/master")
            os.system(cmd)
        ans2 = showinfo("Download started", """The download of DendroPy has started in your default browser.
After pressing OK, select the unzipped 'dendropy' folder to proceed with the installation.""", parent=self)
        if ans2: select_dendropy_dir()
    else:
        ans2 = askyesno("Library dendropy required", """Install 'dendropy' from local directory?""", parent=self,
                        default='no')
        if ans2:
            select_dendropy_dir()


# try to load dendropy
def conf_CIPRES_ID():
    try:  # CHECK CIPRES
        import requests
        import xml.etree.ElementTree as ET
        import python_cipres
    except:
        # ans = askyesno("Warning", "python_cipres library not found, do you want to install it now? This step is only required once.", parent=self)
        print "In conf_CIPRES_ID(): Installing necessary library..."
        import write_cipres_conf
    # write_cipres_conf.install_python_cipres()

    import write_cipres_conf
    write_cipres_conf.exc_panel()


def do_CIPRES_actions(argument):
    try:  # CHECK CIPRES CONFIG FILE
        from os.path import expanduser
        home = expanduser("~")
        conf_file = os.path.normpath("%s/pycipres.conf" % home)
        f = open(conf_file, 'r')
    except(IOError):
        ans = askyesno("Warning",
                       "No CIPRES config file found, do you want to set it up now? This step is only required once.",
                       parent=self)
        if not ans:
            return
        conf_CIPRES_ID()

    try:
        ##import python_cipres ## commented by Madhu
        import client as CipresClient
        properties = CipresClient.Application().getProperties()

        ## Added by Madhu
        print "APPNAME: " + properties.APPNAME
        print "APPID: " + properties.APPID
        ##print properties.USERNAME
        ##print properties.PASSWORD
        print "URL: " + properties.URL
        ## End block Madhu

        client = CipresClient.Client(properties.APPNAME, properties.APPID, properties.USERNAME, properties.PASSWORD,
                                     properties.URL)  #
    except:
        print "In do_CIPRES_actions(): Error loading CipresClient"

    if argument == 'run_CIPRES_test':
        def deleteJobs(var_list, jobs, window):
            count = 0
            for var in var_list:
                if var.get() == 1:
                    count += 1
            if count == 0:
                return
            ans = askyesno("Delete Jobs", "Are you sure you want to delete %s jobs?" % count, parent=window)
            if not ans:
                return
            for var, job in zip(var_list, jobs):
                if var.get() == 1:
                    job.delete()
                    print "deleted!"
            window.destroy()
            update_jobs_gui()



        def downloadJobs(var_list, jobs):
            count = 0
            for var in var_list:
                if var.get() == 1:
                    count += 1
            if count == 0:
                return
            update_bar("Downloading the results, check Console to see the progress...")
            resultsdir = askdirectory(title="Select folder")  # , parent=self)
            for var, job in zip(var_list, jobs):
                if var.get() == 1:
                    new_dir = os.path.normpath("%s/%s" % (resultsdir, job.metadata['clientJobName'].replace(" ", "_")))
                    num = 0
                    while os.path.isdir(new_dir):
                        num = num + 1
                        new_dir = new_dir + str(num)
                    if num > 0:
                        showinfo("Name already used",
                                 "Directory name is already being used so it will be called %s" % new_dir, parent=self)
                    os.system("mkdir %s" % new_dir)
                    proc = subprocess.Popen(["mkdir", new_dir], stdout=subprocess.PIPE, shell=True)
                    job.downloadResults(directory=new_dir)
                    print "job downloaded!"
            update_bar("Download completed.")

        ## This method is added by Madhu on November 29, 2016
        ## to support the clear all check boxes functionality
        def clearJobs(var_list, jobs): ## Added by Madhu
            for itemVal in var_list:
                itemVal.set(0)

        ## This method is added by Madhu on November 30, 2016
        ## to support updating the jobs list gui
        def update_jobs(gui):
            gui.destroy()
            update_jobs_gui()

        def update_jobs_gui():
            try:
                jobs = client.listJobs()
            except Exception: ## Added by Madhu

                ### Following block added by Madhu---START---
                print "Rest webservice not accessible."
                import tkMessageBox

                tkMessageBox.showerror("Webservice problem", "Submission to CIPRES failed, please check your "
                                        "login information in file pycipres.conf in your home directory."
                                       " If this doesn't fix the issue, please contact Mark Miller. (mmiller@sdsc.edu)")

                sys.exit(1)
                ### Block added by Madhu---END---

            if len(jobs) == 0:
                showinfo("Job info", "No pending jobs found!", parent=self)
                return
            jobs_gui = Toplevel(bg='light Grey')
            jobs_gui.title('List of CIPRES jobs')
            jobs_gui.resizable(width=FALSE, height=FALSE)
            ##jobs_dict = dict()## commented by Madhu (Redundant)
            jobs_scroll = Scrollbar(jobs_gui)
            jobs_scroll.pack(side=RIGHT, fill=Y)
            jobs_text = Text(jobs_gui, highlightbackground='light Grey')
            jobs_text.pack(fill=BOTH, expand=1)
            jobs_text.config(yscrollcommand=jobs_scroll.set)
            jobs_scroll.config(command=jobs_text.yview)
            jobs_list = []

            for job in jobs:
                isDone = job.isDone()
                if isDone:
                    isDone = "Yes"
                else:
                    isDone = "No"

                isError = job.isError()
                detailed_msg = ""
                detailed_msg += "Job Name: %s" % job.metadata['clientJobName']

                if isError:
                    detailed_msg = "Job (%s) has FAILED!" % job.metadata['clientJobName']
                else:
                    detailed_msg += "\nCompleted: %s" % (isDone)

                ##jobs_dict[detailed_msg] = 0 ## commented by Madhu (Redundant)
                jobs_list.append(detailed_msg)

            checkbuttons_list = []
            var_list = []

            ##for my_key in jobs_dict: ## commented by Madhu (Redundant)
            for my_key in jobs_list: ## Added by Madhu (Right thing to do)
                var = IntVar()
                var_list.append(var)
                if isError:
                    c = Checkbutton(jobs_text, text=my_key, bg='red', variable=var, width=79, justify=LEFT)
                else:
                    ## Following three lines are added by Madhu to make sure that only completed jobs can be downloaded.
                    if "Completed: No" in my_key:
                        c = Checkbutton(jobs_text, text=my_key, bg='light Grey', variable=var, width=79, justify=LEFT, state=DISABLED)
                    else:
                        c = Checkbutton(jobs_text, text=my_key, bg='light Grey', variable=var, width=79, justify=LEFT)
                c.pack(expand=True, fill='both')
                checkbuttons_list.append(c)
                jobs_text.window_create(END, window=c)
                jobs_text.insert(END, "\n\n")

            delete_button = Button(jobs_gui, highlightbackground='light Grey', text='Delete Selected',
                                   command=lambda: deleteJobs(var_list, jobs, jobs_gui))
            download_button = Button(jobs_gui, highlightbackground='light Grey', text='Download Selected',
                                    command=lambda: downloadJobs(var_list, jobs))
            clear_button = Button(jobs_gui, highlightbackground='light Grey', text='Clear All',
                                    command=lambda: clearJobs(var_list, jobs)) ## new button is added by Madhu
            update_button = Button(jobs_gui, highlightbackground='light Grey', text='Update GUI',
                                    command=lambda: update_jobs(jobs_gui)) ## new button is added by Madhu

            delete_button.pack(side=LEFT, padx=25) ## Original one did not have "padx", added by Madhu
            clear_button.pack(side=LEFT, padx=25) ## Added bu Madhu
            update_button.pack(side=LEFT, padx=25) ## Added bu Madhu
            download_button.pack(side=RIGHT, padx=25) ## Original one did not have "padx", added by Madhu
            jobs_text.config(state=DISABLED)


        update_jobs_gui()


############  WINDOW  #############
try:
    parse_default()
except:
    ### from raxmlgui import OS_def ### This line changed by Madhu October 24, 2016
    import OS_def

    parse_default()

self = Tk()
self.geometry("1200x360")
self.title("raxmlGUI 1.5 beta")
col = "#%s" % K[8]
self.config(bg=col)
self.minsize(1000, 320)
self.tk.call('after', 'idle', 'console', 'hide')
current_OS = K[6]
first_start = 0

if current_OS == "none":
    first_start = 1
    parse_default()
    if current_OS == 'Windows':
        icon = os.path.normpath("%s/icon.ico" % self_path)
        self.wm_iconbitmap(icon)

if current_OS == 'Windows':
    icon = os.path.normpath("%s/icon.ico" % self_path)
    self.wm_iconbitmap(icon)


def nada(a):
    pass


def open_short(a):
    try:
        if fileSafe == "": raise
        add_align()
    except:
        open_ali("1")


if current_OS == 'MacOS':
    self.bind("<Command-o>", open_short)
else:
    self.bind("<Control-o>", open_short)


def run_short(a):
    try:
        run("r")
    except:
        pass


if current_OS == 'MacOS':
    self.bind("<Command-r>", run_short)
else:
    self.bind("<Control-r>", run_short)


def pref_short(a): set()


if current_OS == 'MacOS':
    self.bind("<Command-,>", pref_short)
else:
    self.bind("<Control-Shift-P>", pref_short)


def del_short(a): delete()


if current_OS == 'MacOS':
    self.bind("<Command-Shift-K>", del_short)
else:
    self.bind("<Control-Shift-K>", del_short)


def part_short(a): set_partition()


if current_OS == 'MacOS':
    self.bind("<Command-p>", part_short)
else:
    self.bind("<Control-p>", part_short)


def exc_short(a):
    try:
        exc_2()
    except:
        pass


if current_OS == 'MacOS':
    self.bind("<Command-e>", exc_short)
else:
    self.bind("<Control-e>", exc_short)


def help1_short(a):
    try:
        help_module(2)
    except:
        pass


if current_OS == 'MacOS':
    self.bind("<Command-?>", help1_short)
else:
    self.bind("<Control-h>", help1_short)


def exit(a):
    self.destroy


if current_OS == 'MacOS':
    self.bind("<Command-q>", exit)
else:
    self.bind("<Control-q>", exit)


def export_ali(a):
    try:
        export()
    except:
        pass


if current_OS == 'MacOS':
    self.bind("<Command-s>", export_ali)
else:
    self.bind("<Control-s>", export_ali)


def import_F_short(a):
    try:
        import_fasta()
    except:
        pass


if current_OS == 'MacOS':
    self.bind("<Command-f>", import_F_short)
else:
    self.bind("<Control-f>", import_F_short)


def convert_matrix_short(a):
    try:
        convert_matrix('nex2phy')
    except:
        pass


if current_OS == 'MacOS':
    self.bind("<Command-n>", convert_matrix_short)
else:
    self.bind("<Control-n>", convert_matrix_short)

framme = Tkinter.Frame(self, relief=FLAT, borderwidth=0, highlightbackground='dark blue')
framme.pack(fill=X, expand=NO, side=BOTTOM)
framme.config(bg=col)

### MENU
from sys import version_info

version_info = list(version_info)
weird_menu = 0
# if version_info[0:3] ==[2,7,2]: weird_menu=1

self.option_add('*tearOff', FALSE)
menu = Menu(self)
self.config(menu=menu)

editmenu = Menu(menu, tearoff=0)  # FILE

if current_OS == 'MacOS':
    if weird_menu == 1:
        editmenu.add_command(label='Preferences...', command=set)  # , accelerator="Command-,")
    else:
        editmenu.add_command(label='Preferences...', command=set, accelerator="Command-,")
else:
    editmenu.add_command(label='Preferences...', command=set, accelerator="Ctrl+Shift+P")

editmenu.add_separator()
dtypeM = Menu(editmenu)

if current_OS == 'MacOS':
    if weird_menu == 1:
        editmenu.add_command(label='Load alignment',
                             command=lambda: open_ali('1'))  # , accelerator="Command-O") #command=open)
        editmenu.add_command(label='Add new alignment', command=add_align, state=DISABLED)  # ,accelerator="O")
        # utimenu.add_command(label='Import NEXUS file', command=lambda: convert_matrix('nex2phy')) Line changed by Madhu
        editmenu.add_command(label='Import NEXUS file', command=lambda: convert_matrix('nex2phy'))
        editmenu.add_command(label='Import FASTA file', command=import_fasta)

    else:
        editmenu.add_command(label='Load alignment', command=lambda: open_ali('1'),
                             accelerator="Command-O")  # command=open)
        editmenu.add_command(label='Add new alignment', command=add_align, state=DISABLED, accelerator="Command-O")
        editmenu.add_command(label='Import NEXUS file', command=lambda: convert_matrix('nex2phy'),
                             accelerator="Command-N")
        editmenu.add_command(label='Import FASTA file', command=import_fasta, accelerator="Command-F")

else:
    editmenu.add_command(label='Load alignment', command=lambda: open_ali('1'), accelerator="Ctrl+O")  # command=open)
    editmenu.add_command(label='Add new alignment', command=add_align, state=DISABLED, accelerator="Ctrl+O")
    editmenu.add_command(label='Import NEXUS file', command=lambda: convert_matrix('nex2phy'), accelerator="Ctrl+N")
    editmenu.add_command(label='Import FASTA file', command=import_fasta, accelerator="Ctrl+F")

editmenu.add_cascade(label='Set Data Type', menu=dtypeM)  # ,state=DISABLED)
dtyp = StringVar()
dtypeM.add_radiobutton(label='DNA', variable=dtyp, value="DNA", command=mod_tools2)
dtypeM.add_radiobutton(label='Binary', variable=dtyp, value="BIN", command=mod_tools2)
dtypeM.add_radiobutton(label='Multistate', variable=dtyp, value="MULTI", command=mod_tools2)
dtypeM.add_radiobutton(label='AA', variable=dtyp, value="AA", command=mod_tools2)
dtypeM.add_radiobutton(label='Mixed', variable=dtyp, value="MIXED", command=mod_tools2)

# editmenu.add_command(label='Edit alignment', command=edit,state=DISABLED)		#
# if current_OS=='MacOS':
#	if weird_menu==1: editmenu.add_command(label='Save and reload alignment', command=export)
#	else: editmenu.add_command(label='Save and reload alignment', command=export,accelerator="Command-S",state=DISABLED)	#
# else: editmenu.add_command(label='Save and reload alignment', command=export,accelerator="Ctrl+S",state=DISABLED)
# editmenu.add_command(label='Show RAxML command', command=lambda: run('e'),state=DISABLED)

wrapT = Menu(editmenu)
editmenu.add_cascade(label='Alignment view', menu=wrapT)


def wrap(arg):
    texxt.config(wrap=arg)


wrapT.add_radiobutton(label='Wrap lines', command=lambda: wrap('char'))
wrapT.add_radiobutton(label="Don't wrap lines", command=lambda: wrap('none'))

if current_OS == 'MacOS':
    if weird_menu == 1:
        editmenu.add_command(label='Clear', command=delete)  # , accelerator="Command-Shift-K")
    else:
        editmenu.add_command(label='Clear', command=delete, accelerator="Command-Shift-K")
else:
    editmenu.add_command(label='Clear', command=delete, accelerator="Ctrl+Shift+K")

editmenu.add_separator()

if current_OS == 'MacOS':
    if weird_menu == 1:
        editmenu.add_command(label='Quit', command=self.destroy)  # , accelerator="Q")
    else:
        editmenu.add_command(label='Quit', command=self.destroy, accelerator="Command-Q")
else:
    editmenu.add_command(label='Quit', command=self.destroy, accelerator="Ctrl+Q")

menu.add_cascade(label="File", menu=editmenu)

optmenu = Menu(self)  # OPTIONS
optmenu.add_command(label='Select multiple outgroup...', command=lambda: constraint('6'),
                    state=DISABLED)  # EXCLUDE SITES

if current_OS == 'MacOS':
    if weird_menu == 1:
        optmenu.add_command(label='Exclude sites...', command=exc_2, state=DISABLED)  # , accelerator="E")
    else:
        optmenu.add_command(label='Exclude sites...', command=exc_2, state=DISABLED, accelerator="Command-E")
else:
    optmenu.add_command(label='Exclude sites...', command=exc_2, state=DISABLED, accelerator="Ctrl+E")

if current_OS == 'MacOS':
    if weird_menu == 1:
        optmenu.add_command(label='Set/Edit partitions...', command=set_partition, state=DISABLED)  # , accelerator="P")
    else:
        optmenu.add_command(label='Set/Edit partitions...', command=set_partition, state=DISABLED,
                            accelerator="Command-P")
else:
    optmenu.add_command(label='Set/Edit partitions...', command=set_partition, state=DISABLED, accelerator="Ctrl+P")

optmenu.add_command(label='Delete partitions', command=del_partition, state=DISABLED)  # PARTITIONS
optmenu.add_command(label='Export partition file', command=export_part, state=DISABLED)  # PARTITIONS

optmenu.add_separator()

if current_OS == 'MacOS':
    if weird_menu == 1:
        optmenu.add_command(label='Save memory search (-F)', command=use_F, state=DISABLED)  # , accelerator="F")
    else:
        optmenu.add_command(label='Save memory search (-F)', command=use_F, state=DISABLED)
else:
    optmenu.add_command(label='Save memory search (-F)', command=use_F, state=DISABLED)

optmenu.add_separator()

mButt0 = Menu(optmenu)
optmenu.add_cascade(label='Load additional files...', menu=mButt0, state=DISABLED)
mButt0.add_command(label='Load secondary structure...', command=sec_str)  # PARTITIONS
mButt0.add_command(label='Load starting tree', command=lambda: constraint('3'))

mButt1 = Menu(optmenu)
optmenu.add_cascade(label='Enforce constraint...', menu=mButt1, state=DISABLED)
mButt1.add_command(label='Load binary constraint', command=lambda: constraint('1'))
mButt1.add_command(label='Load multifurcating constraint', command=lambda: constraint('2'))
mButt1.add_command(label='Define topological constraint...', command=lambda: constraint('4'))

mButt2 = Menu(optmenu)
optmenu.add_cascade(label='Consensus trees...', menu=mButt2)
mButt2.add_command(label='Majority rule', command=lambda: consensus('MR'))
mButt2.add_command(label='Extended majority rule', command=lambda: consensus('MRE'))
mButt2.add_command(label='Strict consensus', command=lambda: consensus('STRICT'))
mButt2.add_command(label='Majority rule - Dropset', command=lambda: consensus('MR_DROP'))
mButt2.add_command(label='Strict consensus - Dropset', command=lambda: consensus('STRICT_DROP'))
# mButt2.add_separator()
# mButt2.add_command(label='Convert to FigTree format', command=lambda: consensus('RE_conv'))

mButt3 = Menu(optmenu)
optmenu.add_cascade(label='Additional analyses...', menu=mButt3)
mButt3.add_command(label='Robinson Foulds tree distances', command=Foulds)
mButt3.add_command(label='Per site log Likelihoods', command=CONSEL, state=DISABLED)  # PARTITIONS
mButt3.add_command(label='SH-like support value computation', command=SH, state=DISABLED)  # PARTITIONS
menu.add_cascade(label="Analysis", menu=optmenu)

######################################################################
utimenu = Menu(self, tearoff=0)  # UTILITIES

utimenu.add_command(label='Edit alignment', command=edit, state=DISABLED)  #

if current_OS == 'MacOS':
    if weird_menu == 1:
        utimenu.add_command(label='Save and reload alignment', command=export, state=DISABLED)
    else:
        utimenu.add_command(label='Save and reload alignment', command=export, accelerator="Command-S",
                            state=DISABLED)  #
else:
    utimenu.add_command(label='Save and reload alignment', command=export, accelerator="Ctrl+S", state=DISABLED)

utimenu.add_command(label='Show RAxML command', command=lambda: run('e'), state=DISABLED)
utimenu.add_command(label='Export NEXUS file', command=lambda: convert_matrix('phy2nex'))
utimenu.add_command(label='Convert tree file to FigTree format...', command=lambda: consensus('RE_conv'))

utimenu.add_separator()

d = Menu(utimenu)
utimenu.add_cascade(label='Export citation', menu=d)
d.add_radiobutton(label='Text file', command=lambda: help_module(10))
d.add_radiobutton(label='EndNote (XML)', command=lambda: help_module(7))
d.add_radiobutton(label='Reference manager (RIS)', command=lambda: help_module(8))
d.add_radiobutton(label='BibTeX library', command=lambda: help_module(9))

utimenu.add_command(label='Configure CIPRES ID', command=conf_CIPRES_ID)

menu.add_cascade(label="Utilities", menu=utimenu)
######################################################################

helpmenu = Menu(self)  # HELP
helpmenu.add_command(label='About raxmlGUI', command=lambda: help_module(1))

if current_OS == 'MacOS':
    if weird_menu == 1:
        helpmenu.add_command(label='Help raxmlGUI', command=lambda: help_module(2))  # , accelerator="?")
    else:
        helpmenu.add_command(label='Help raxmlGUI', command=lambda: help_module(2), accelerator="Command-?")
else:
    helpmenu.add_command(label='Help raxmlGUI', command=lambda: help_module(2), accelerator="Ctrl+H")

helpmenu.add_command(label='Help RAxML', command=lambda: help_module(3))
# helpmenu.add_command(label='Save log to file...', command=lambda: help_module(6))

helpmenu.add_separator()
helpmenu.add_command(label='Join raxmlGUI mailing list...', command=lambda: help_module(6))
helpmenu.add_command(label='Find updates raxmlGUI...', command=lambda: help_module(4))
helpmenu.add_command(label='Find updates RAxML...', command=lambda: help_module(5))
menu.add_cascade(label="Help", menu=helpmenu)

### STAUTS BAR
if current_OS == 'MacOS':    Label(framme, text='  ', bg=col).pack(side=RIGHT)

try:
    import multiprocessing

    nthr = multiprocessing.cpu_count()
    listP = range(2, nthr + 1)
    if len(listP) < 1: raise
except:
    listP = range(2, 21)

proc = StringVar()  # DEFINE NUMBER PROCESSORS

#### In following block opt chabged to opt2A to have a control over the it's visibility by Madhu ####
opt2A = apply(OptionMenu, (framme, proc) + tuple(listP[::1]))
opt2A.pack(side=RIGHT)
opt2A.config(bg=col)
#### End block: opt chabged to opt2A to have a control over the it's visibility by Madhu ####
proc.set(K[1])

##Label(framme, text=' n. threads', bg=col).pack(side=RIGHT) Commented by Madhu and replaced by follwoing 2 lines
n_threads=Label(framme, text=' n. threads', bg=col) ## Added by Madhu
n_threads.pack(side=RIGHT) ## Added by Madhu

n_threads.config(state=DISABLED) ## Added by Madhu
opt2A.config(state=DISABLED) ## Added by Madhu

global frame2
frame2 = Tkinter.Frame(framme, relief=FLAT, borderwidth=1)
frame2.pack(fill=X, expand=NO, side=LEFT)
frame2.config(bg=col)
raxV = "%s" % K[0]
Label(frame2, text=raxV, fg='dark blue', bg=col).pack(side=RIGHT)

cipres_cpu_time = StringVar()  # DEFINE CIPRES-REST CPU TIME
opt2 = apply(OptionMenu, (framme, cipres_cpu_time) + tuple([0.5, 1, 2, 4, 8, 12, 16, 24, 48, 72, 96, 120, 144, 168]))
opt2.pack(side=RIGHT)
opt2.config(bg=col)
cipres_cpu_time.set(1)
## Label(framme, text='    CIPRES runtime (h)', bg=col).pack(side=RIGHT) ## Commented by Madhu and replaced by follwoing 2 lines
runtime_inhrs=Label(framme, text='    runtime (h)', bg=col)## Added by Madhu
runtime_inhrs.pack(side=RIGHT)## Added by Madhu

##localrun=Label(framme, text='Local run only:', bg=col) ## Added by Madhu and then commented out
##localrun.pack(side=RIGHT)## Added by Madhu and then commented out
##localrun.config(state=DISABLED) ## Added by Madhu and then commented out

##runtime_inhrs.config(state=DISABLED) ## Added by Madhu and commented later on
##opt2.config(state=DISABLED) ## Added by Madhu and commented later on

# global frame2
# frame2 = Tkinter.Frame(framme, relief=FLAT, borderwidth=1)
# frame2.pack(fill=X, expand=NO, side=LEFT)
# frame2.config(bg=col)
# raxV= "%s" % K[0]
# Label(frame2, text=raxV, fg= 'dark blue', bg = col).pack(side=RIGHT)
#



### MAIN TOOLBAR
fram = Frame(self, relief=RAISED, borderwidth=1)
fram.pack(fill=X, expand=NO)
frame = Frame(fram)
frame.pack(fill=X, expand=NO, side=TOP)
frame.config(bg=col)
v = IntVar()
Label(frame, text=' ', bg=col).pack(side=LEFT)
button2 = Button(frame)  # Load alignment
button2.pack(side=LEFT)
button2.config(highlightbackground=col, text='Load alignment', padx=20, pady=2, command=lambda: open_ali('1'))

frrr = Frame(frame)
frrr.pack(fill=X, expand=NO, side=LEFT)
frrr.config(bg=col)
Label(frrr, text=' ', bg=col).pack(side=LEFT)
entry = Entry(frrr, width=15) ## original width=20 changed by Madhu

outfile = StringVar()
entry["textvariable"] = outfile
entry.pack(side=LEFT)

if current_OS == 'MacOS':
    entry.config(font=(11), bg='white', fg='dark blue', highlightthickness=0)
else:
    entry.config(bg='white', fg='dark blue', highlightthickness=0)

entry.focus_set()
outfile.set('outfile')

button5 = Button(frame, text='Run RAxML locally', padx=20, pady=2, command=lambda: run('r'))  # RUN RAXML
button5.pack(side=RIGHT)
button5.config(highlightbackground=col, state=DISABLED)


### CIPRES-REST OPTIONS
# __ button7 = Button(frame, text='Cipres RAxML', padx=20, pady=2, command=lambda: run('run_CIPRES')) # RUN RAXML
# __ button7.pack(side=RIGHT)
# __ button7.config(highlightbackground = col, state=DISABLED)

def def_CIPRES_action(value):
    try:
        if value == "Run CIPRES-RAxML":
            run('run_CIPRES')  ###
        elif value == "Run CIPRES-RAxML in background":
            run('run_CIPRES_background')
        elif value == "Check CIPRES Jobs":
            do_CIPRES_actions('run_CIPRES_test')
    except:
        pass
    cipres_action.set("Use CIPRES")


cipres_action = StringVar()

## button8 definitaion shown below commented by Madhu on December 16, 2016 to remove 'Run CIPRES-RAxML'
##  from drop down. This option though fully functional causes confusion. 'Run CIPRES-RAxML in background' can do
## the job in more elegant way with less confusion to the user.
##button8 = OptionMenu(frame, cipres_action, 'Run CIPRES-RAxML', 'Run CIPRES-RAxML in background', 'Check CIPRES Jobs',
##                     command=def_CIPRES_action)
button8 = OptionMenu(frame, cipres_action, 'Run CIPRES-RAxML in background', 'Check CIPRES Jobs', command=def_CIPRES_action)

button8.pack(side=RIGHT)
cipres_action.set("Use CIPRES")

if current_OS == 'Windows':
    button8.config(bg=col, width=28)  # , justify=RIGHT)  ## width changed from 23 to 28 by Madhu
else:
    button8.config(bg=col, width=18)  # , width =len(def_a))#, justify=RIGHT)

## Following three lines are commented here by Madhu and they are copied somewhat later in the code
##button6 = Tkinter.Button(frame, text='Clear', padx=25, pady=2, command=delete)
##button6.pack(side=RIGHT)
##button6.config(highlightbackground=col, state=DISABLED)

def def_changeResource(value):
    try:
        if value == "Use RAxML locally":
            button8.config(highlightbackground = col, state=DISABLED)
            button5.config(highlightbackground = col, state=NORMAL)
            opt2A.config(state=NORMAL)
            opt2.config(state=DISABLED)
            runtime_inhrs.config(state=DISABLED)
            n_threads.config(state=NORMAL)
            ###localrun.config(state=NORMAL)
        elif value == "Use CIPRES":
            button5.config(highlightbackground = col, state=DISABLED)
            button8.config(highlightbackground = col, state=NORMAL)
            opt2A.config(state=DISABLED)
            opt2.config(state=NORMAL)
            runtime_inhrs.config(state=NORMAL)
            n_threads.config(state=DISABLED)
            ###localrun.config(state=DISABLED)

    except:
        pass
    change_resouce.set("Change resource")

change_resouce = StringVar()
button6A = OptionMenu(frame, change_resouce, 'Use CIPRES', 'Use RAxML locally',
                     command=def_changeResource)
button6A.config(bg = "light GREY")
button6A.pack(side=RIGHT)
change_resouce.set("Change resource")
button6A.config(bg=col, width=15)


## Following three lines are copied here by Madhu to place the Clear button at position suggested by Mark
button6 = Tkinter.Button(frame, text='Clear', padx=25, pady=2, command=delete)
button6.pack(side=RIGHT)
button6.config(highlightbackground=col, state=DISABLED)


### SECOND TOOLBAR
def def_BS(a):
    global BSrep, toolbR, save_brL, toolbR2, BSrep2
    opt5.config(bg=col, width=len(str(a)) + 3)
    if a == "User defined...":
        try:
            toolbR.destroy()
            toolbR2.destroy()
        except:
            pass

        toolbR = Frame(toolbA)
        toolbR.pack(fill=X, expand=NO, side=RIGHT)
        toolbR.config(bg=col)
        BSrep = StringVar()
        Label(toolbR, text='reps. ', bg=col).pack(side=LEFT)

        entry = Entry(toolbR, width=10)
        BSrep = StringVar()
        entry["textvariable"] = BSrep
        entry.pack(side=LEFT)
        if current_OS == 'MacOS':
            entry.config(font=(11), bg='white', fg='dark blue', highlightthickness=0)
        else:
            entry.config(bg='white', fg='dark blue', highlightthickness=0)
        entry.focus_set()
        save_brL = StringVar()
        onn = "-k"
        check1k = Checkbutton(toolbR, text="BS brL", variable=save_brL, onvalue=onn, offvalue=" ")
        check1k.pack(side=RIGHT)
        check1k.config(bg=col)
        check1k.deselect()
        value = replicate.get()
        if value == 'ML + thorough bootstrap' or K[
            3] == 'thorough' and value != 'ML + rapid bootstrap' and value != 'ML search' and value != 'Ancestral states':
            toolbR2 = Frame(toolbA)
            toolbR2.pack(fill=X, expand=NO, side=RIGHT)
            toolbR2.config(bg=col)
            BSrep2 = StringVar()
            name = Label(toolbR2, text=' runs', bg=col).pack(side=LEFT)  # DEFINE NUMBER BS REPLICATES
            listREP2 = '1', '10', '20', '50', '100'
            got = '1'
            opt6 = apply(OptionMenu, (toolbR2, BSrep2) + tuple(listREP2[::1]))
            BSrep2.set(got)
            opt6.pack(side=LEFT)
            opt6.config(bg=col)  # , width =1)


def def_ST(a):
    global const_f
    if a == "User defined":
        constraint('3')
    else:
        const_f == ''


def def_analysis(value):
    global BSrep, opt5, listREP, toolbR, BSrep2, toolbR2, save_brL, button_load_tree, rooted_tree
    rooted_tree = ""
    opt4.config(bg=col, width=len(str(value)))
    try:
        toolbR.destroy()
    except:
        pass
    try:
        toolbR2.destroy()
    except:
        pass
    toolbR = Frame(toolbA)
    toolbR.pack(fill=X, expand=NO, side=RIGHT)
    toolbR.config(bg=col)
    BSrep = StringVar()

    # if value == 'ML + rapid bootstrap':
    # 	button8.config(state=NORMAL)

    if value == 'Ancestral states':
        button_load_tree = Button(toolbR)  # Load alignment
        button_load_tree.pack(side=LEFT)
        button_load_tree.config(highlightbackground=col, text='Load tree file', pady=2,
                                command=lambda: open_rooted_tree())
        try:
            frame3.destroy()
        except:
            pass
        ##button5.config(state=DISABLED) ## Commented by Madhu 'Make Selection' should enable it
        # __ button7.config(state=DISABLED)
        # button6.config(state=DISABLED)
        got = '1'

    elif value == 'Pairwise distances':
        name = Label(toolbR, text=' starting tree', bg=col).pack(side=LEFT)  # DEFINE NUMBER BS REPLICATES
        boh = StringVar()
        opt5 = OptionMenu(toolbR, boh, 'Maximum parsimony', 'User defined', command=def_ST)
        opt5.pack(side=LEFT)
        try:
            frame3.destroy()
            opt5.config(state=DISABLED)

        except:
            opt5.config(state=DISABLED)
        # button5.config(state=DISABLED)
        # button6.config(state=DISABLED)
        boh.set('Maximum parsimony')
        opt5.config(bg=col, width=len('Maximum parsimony'))
        got = '1'
        try:
            if fileinputS != "":
                mod_tools()
                opt5.config(state=NORMAL)
        except:
            pass


    elif value == 'ML search':
        save_brL = StringVar()
        onn = "brl"
        check1k = Checkbutton(toolbR, text="combined output", variable=save_brL, onvalue=onn, offvalue=" ")
        check1k.pack(side=RIGHT)
        check1k.config(bg=col)
        check1k.deselect()
        BSrep = StringVar()
        onn = "sh"
        check2k = Checkbutton(toolbR, text="SH-like values", variable=BSrep, onvalue=onn, offvalue=" ")
        check2k.pack(side=RIGHT)
        check2k.config(bg=col)
        check2k.deselect()

        name = Label(toolbR, text=' runs', bg=col).pack(side=LEFT)  # DEFINE NUMBER BS REPLICATES
        # listREP='1', '10', '20', '50', '100', '500'
        got = '1'
        BSrep2 = StringVar()
        opt5 = OptionMenu(toolbR, BSrep2, '1', '10', '20', '50', '100', '500', command=def_BS)
        opt5.pack(side=LEFT)
        BSrep2.set(got)
        opt5.config(bg=col)
        try:
            s = file(fileinputS, 'r')
            taxa_list(s)
        except:
            pass

    elif value == 'Fast tree search':
        BSrep = StringVar()
        onn = "sh"
        check2k = Checkbutton(toolbR, text="SH-like values", variable=BSrep, onvalue=onn, offvalue=" ")
        check2k.pack(side=RIGHT)
        check2k.config(bg=col)
        check2k.deselect()
        save_brL = StringVar()
        onn = "brl"
        check1k = Checkbutton(toolbR, text="compute brL", variable=save_brL, onvalue=onn, offvalue=" ")
        check1k.pack(side=RIGHT)
        check1k.config(bg=col)
        check1k.deselect()
        try:
            s = file(fileinputS, 'r')
            taxa_list(s)
        except:
            pass
    elif value == 'RELL bootstraps':
        save_brL = StringVar()
        onn = "-k"
        check1k = Checkbutton(toolbR, text="BS brL", variable=save_brL, onvalue=onn, offvalue=" ")
        check1k.pack(side=RIGHT)
        check1k.config(bg=col)
        check1k.deselect()
    else:  ## for ML + rapid bootstrap && bootstrap + consensus
        name = Label(toolbR, text=' reps.', bg=col).pack(side=LEFT)  # DEFINE NUMBER BS REPLICATES
        listREP = '100', '200', '500', '1000', '10000', 'autoMR', 'autoMRE', 'autoMRE_IGN', 'autoFC', 'User defined...'
        got = K[4]
        BSrep = StringVar()
        opt5 = OptionMenu(toolbR, BSrep, '100', '200', '500', '1000', '10000', 'autoMR', 'autoMRE', 'autoMRE_IGN',
                          'autoFC', 'User defined...', command=def_BS)
        opt5.pack(side=LEFT)
        BSrep.set(got)
        opt5.config(bg=col, width=10)
        try:
            s = file(fileinputS, 'r')
            taxa_list(s)
        except:
            pass

        save_brL = StringVar()
        onn = "-k"
        check1k = Checkbutton(toolbR, text="BS brL", variable=save_brL, onvalue=onn, offvalue=" ")
        check1k.pack(side=RIGHT)
        check1k.config(bg=col)
        check1k.deselect()

    # if value != 'Ancestral states' or value != 'Pairwise distances': pass
    # opt5 = apply(OptionMenu, (toolbR, BSrep) + tuple(listREP[::1]))
    # BSrep.set(got)
    # opt5.pack(side=LEFT)
    # opt5.config(bg = col, command=def_BS)
    if value == 'ML + thorough bootstrap' or K[
        3] == 'thorough' and value != 'ML + rapid bootstrap' and value != 'ML search' and value != 'Ancestral states':
        toolbR2 = Frame(toolbA)
        toolbR2.pack(fill=X, expand=NO, side=RIGHT)
        toolbR2.config(bg=col)
        BSrep2 = StringVar()
        name = Label(toolbR2, text=' runs', bg=col).pack(side=LEFT)  # DEFINE NUMBER BS REPLICATES
        listREP2 = '1', '10', '20', '50', '100'
        got = '10' ## original got = '1' was changed by Madhu because in this option number of runs have to be > 1
        opt6 = apply(OptionMenu, (toolbR2, BSrep2) + tuple(listREP2[::1]))
        BSrep2.set(got)
        opt6.pack(side=LEFT)
        opt6.config(bg=col, width=5)
        # opt6.config(bg = col)#, width =1)


toolb = Frame(fram)
toolb.pack(fill=X, expand=NO, side=TOP)
toolb.config(bg=col)
toolbA = Frame(toolb)
toolbA.pack(fill=X, expand=NO, side=LEFT)
toolbA.config(bg=col)
Label(toolbA, text=' ', bg=col).pack(side=LEFT)  # DEFINE BS RAPID/THROUGH
replicate = StringVar()
opt4 = OptionMenu(toolbA, replicate, 'Fast tree search', 'ML search', 'ML + rapid bootstrap', 'ML + thorough bootstrap', \
                  'Bootstrap + consensus', 'Ancestral states', 'Pairwise distances', 'RELL bootstraps',
                  command=def_analysis)
opt4.pack(side=LEFT)

if K[3] == 'rapid' or K[3] == 'thorough':
    def_a = "ML + %s bootstrap" % K[3]
    def_analysis(K[3])
else:
    def_a = "%s search" % K[3]

replicate.set(def_a)

if current_OS == 'Windows':
    opt4.config(bg=col, width=23)  # , justify=RIGHT)
else:
    opt4.config(bg=col, width=len(def_a))  # , justify=RIGHT)

def_analysis(replicate)


def a_short(a):
    w = replicate.get()
    if w == "RELL bootstraps":
        replicate.set("RELL bootstraps")
        def_analysis("RELL bootstraps")

    if w == "ML search":
        replicate.set("ML + rapid bootstrap")
        def_analysis("ML + rapid bootstrap")

    if w == "ML + rapid bootstrap":
        replicate.set("ML + thorough bootstrap")
        def_analysis("ML + thorough bootstrap")

    if w == "ML + thorough bootstrap":
        replicate.set("Bootstrap + consensus")
        def_analysis("Bootstrap + consensus")

    if w == "Bootstrap + consensus":
        replicate.set("Ancestral states")
        def_analysis("Ancestral states")

    if w == "Ancestral states":
        replicate.set("Fast tree search")
        def_analysis("Fast tree search")

    if w == "Fast tree search":
        replicate.set("Pairwise distances")
        def_analysis("Pairwise distances")

    if w == "Pairwise distances":
        replicate.set("ML search")
        def_analysis("ML search")


if current_OS == 'MacOS':
    self.bind("<Command-a>", a_short)
else:
    self.bind("<Control-a>", a_short)

#### TEXT
frame = Frame(self)  # , bd=2, relief=SUNKEN)

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=E + W)

yscrollbar = Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=N + S)

texxt = Text(frame, bd=0,
             xscrollcommand=xscrollbar.set,
             yscrollcommand=yscrollbar.set,
             highlightthickness=0, wrap=K[9])

texxt.config(padx=10, pady=0, font=('Monaco', 10), relief=GROOVE, bg='#e6e6e6', fg='dark blue')
texxt.grid(row=0, column=0, sticky=N + S + E + W)
xscrollbar.config(command=texxt.xview)
yscrollbar.config(command=texxt.yview)

frame.pack(side=TOP, expand=YES, fill=BOTH)
# texxt.pack(side=TOP, expand=YES)#, fill=BOTH)

texxt.config(state=DISABLED)

# if __name__ == '__main__': ScrolledText().mainloop()
delete()

if first_start == 1:
    import help
    help.beta_info(current_OS)

###### Added by Madhu ######
## Block start to postion the GUI correctly

self.withdraw()
self.update_idletasks()  # Update "requested size" from geometry manager

screen_width = self.winfo_screenwidth()
screen_height = self.winfo_screenheight()

##print "GUI width: " + str(self.winfo_width())

screenX = (screen_width - 1200) / 2 ## width 1200 is set explicitly when GUI is created
##screenY = (screen_height - self.height) / 2
screenY = 30
self.geometry("+%d+%d" % (screenX, screenY))

# This seems to draw the window frame immediately, so only call deiconify()
# after setting correct window position
self.deiconify()

## Block end to postion the GUI correctly


###### Added by Madhu ######
"""Three lines after this comment are added by Madhu to make sure that main GUI is on the top when it launches
and it lets children come on the top when they are launched"""
self.lift()
self.attributes('-topmost',True)
self.after_idle(self.attributes,'-topmost',False)
###### Added by Madhu ######

self.mainloop()

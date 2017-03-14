#!/usr/bin/env python
# raxmlGUI 0.93 build 20100730. A graphical front-end for RAxML.
# Created by Daniele Silvestro on 20/01/2010. => dsilvestro@senckenberg.de
import os
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *

# MAC
# self_path =os.path.join(os.path.split(__file__)[0]) # is the path of this file
self_path = os.getcwd()  # gives the path of this script if you run it from terminal
# print "\n\t", self_path, "\n"
self_path = "%s/raxmlgui" % self_path
raxml_path = """ "%s/raxml" """ % self_path


def read_pref():
    global K, pref, current_OS, raxmlv, Xterminal
    pref = "%s/defaults" % self_path
    pref = file(pref, 'r')
    f = pref.readlines()  # DEFINING OUTGROUP
    K = list()  # R[start:stop:step]
    j = 0
    for i in f:
        param = i.split()
        if len(param) > 2:
            K.insert(j, param[1] + " " + param[2])
        else:
            K.insert(j, param[1])  # the second is picked as parameter
        j = j + 1

    raxmlv = K[0]

    ###### Block start added by Madhu ######
    from sys import platform as _platform

    if _platform == "linux" or _platform == "linux2":
         K[6] = "Linux"
    elif _platform == "darwin":
        K[6] = "MacOS"
    elif _platform == "win32":
        K[6] = "Windows"
    ###### Block end added by Madhu ######

    current_OS = K[6]
    Xterminal = K[7]


try:
    import multiprocessing

    global nthr
    nthr = multiprocessing.cpu_count()
    listP = range(2, nthr + 1)

    if len(listP) < 1:
        raise

except:
    listP = range(2, 21)


def find():
    read_pref()

    def noset_pref(a):
        import main
        main.update_menu('pref_on')
        master.destroy()

    def noset_pref_0():
        import main
        main.update_menu('pref_on')
        master.destroy()

    def warn():
        ans = askyesno("Preferences changed", "You must restart raxmlGUI to make the changes effective. Restart now?",
                       parent=master)
        if ans:
            from main import restart_me
            restart_me()

    def set_pref(a):
        outfile = "%s/defaults" % self_path
        outfile = file(outfile, 'w')
        pref = "%s/defaults" % self_path
        pref = file(pref, 'r')
        pref_def = """RAxML_version: %s
Number_processors: %s 
Substitution_Model: %s 
Analysis: %s 
BS_replicates: %s 
open_MLtree: %s
OS: %s
Term: %s
Toolbar_color: %s
Wrap_line: %s""" % (
            ver.get(), proc.get(), "GTRGAMMA", replicate.get(), BSrep.get(), openML.get(), OS.get(), Term.get(), K[8],
            K[9])
        outfile.writelines(pref_def)
        warn()
        noset_pref(0)

    def restore():
        outfile = "%s/defaults" % self_path
        outfile = file(outfile, 'w')
        pref = "%s/defaults" % self_path
        pref = file(pref, 'r')
        pref_def = """RAxML_version: raxmlHPC-none
Number_processors: 2 
Substitution_Model: GTRGAMMA 
Analysis: rapid bootstrap 
BS_replicates: 100 
open_MLtree: no
OS: none
Term: Terminal
Toolbar_color: DBDBDB
Wrap_line: none"""
        outfile.writelines(pref_def)
        outfile.close()
        warn()
        noset_pref(0)

    def raxmlV():  # add a new version of RAxML
        (fileinput) = askopenfilename(title="Load RAxML executable")

        if fileinput:
            s = file(fileinput)
            raxmlV_file = "%s" % fileinput

            if current_OS == 'Windows':
                cmd = """xcopy "%s" %s/Y /F""" % (raxmlV_file, raxml_path)
            else:
                cmd = """cp "%s" %s """ % (raxmlV_file, raxml_path)

            print cmd
            os.system(cmd)
            raxmlv = os.path.basename(raxmlV_file)  # file name print cmd, raxmlv
            print "RAXMLV: " + raxmlv
            list_exe()
            version = raxmlv
            ver.set(version)

    def del_raxmlV():
        w = "Do you want to delete the file '%s'? You can't undo this action." % ver.get()
        ans = askokcancel('Warning', w)

        if ans:
            raxml_exe = ver.get()

            if current_OS == 'Windows':
                cmd = """cd %s && del %s""" % (raxml_path, raxml_exe)
            else:
                cmd = """cd %s && rm %s""" % (raxml_path, raxml_exe)

            print cmd
            os.system(cmd)
            list_exe()

    def list_exe():
        version = "%s" % K[0]
        Label(master, text=' RAxML version', bg="light Grey").grid(row=6, column=0, sticky=W)
        raxDIR = ("%s/raxml") % self_path
        global l, opt, ver
        l = os.listdir(raxDIR)
        L = list()
        for i in l:
            if "pthreadGC2" not in i:
                ## This block makes sure that only OS relevant apps show in drop down
                ### BLOCK START Added by Madhu on December 21, 2016
                if current_OS == 'Windows':
                    if 'Windows' in i:
                        L.append(i)
                if current_OS == 'MacOS':
                    if 'Mac' in i:
                        L.append(i)
                if current_OS == 'Linux':
                    if 'Linux' in i:
                ### BLOCK END Added by Madhu on December 21, 2016
                        L.append(i)

        ver = StringVar()
        opt = apply(OptionMenu, (master, ver) + tuple(L[::1]))  # list binaries

        if current_OS == 'Windows':
            opt.config(bg="light Grey", width=20)
        else:
            opt.config(bg="light Grey", width=20)

        opt.grid(row=6, column=1, sticky=W, columnspan=2)
        ver.set(version)

    master = Toplevel()
    master2 = master
    master.title("Preferences")
    master.geometry("360x235")
    master.protocol("WM_DELETE_WINDOW", noset_pref_0)
    master.config(bg='light Grey')

    if current_OS == 'Windows':
        icon = "%s/icon.ico" % self_path
        master.wm_iconbitmap(icon)
        master.minsize(442, 235) ## master.minsize(342, 235)  ---  changed by Madhu
        ##master.maxsize(442, 235) ## commented by Madhu
        master.resizable ## added bu Madhu
    else:
        master.minsize(490, 235)  ## master.minsize(390, 235)  ---  changed by Madhu
        ##master.maxsize(490, 235)  ## commented by Madhu
        master.resizable ## added by Madhu

    master.grab_set()
    Label(master, text=' Default analysis', bg="light Grey").grid(row=0, column=0, sticky=W)  # DEFINE BS RAPID/THROUGH
    replicate = StringVar()
    opt4 = OptionMenu(master, replicate, 'ML search', 'rapid bootstrap', 'thorough bootstrap')
    opt4.grid(row=0, column=1, sticky=W, columnspan=3)
    replicate.set(K[3])
    opt4.config(bg="light Grey")  # , width =14)

    Label(master, text=' Bootstrap reps', bg="light Grey").grid(row=1, column=0,
                                                                sticky=W)  # DEFINE NUMBER BS REPLICATES
    BSrep = StringVar()
    opt5 = OptionMenu(master, BSrep, 'autoMR', 'autoMRE', 'autoMRE_IGN', 'autoFC', '50', '100', '200', '500', '1000',
                      '10000')
    opt5.grid(row=1, column=1, sticky=W, columnspan=2)
    opt5.config(bg="light Grey")
    BSrep.set(K[4])

    Label(master, text=' Open results', bg="light Grey").grid(row=3, column=0, sticky=W)
    openML = StringVar()
    check1 = Checkbutton(master, text=" ", variable=openML, onvalue="yes", offvalue="no")
    check1.grid(row=3, column=1, sticky=W, columnspan=2)
    check1.config(bg="light Grey")
    # def check1def():

    if K[5] == "yes":
        check1.select()
    elif K[5] == "no":
        check1.deselect()

    def info_open():
        showinfo("Open results",
                 """ML (+ bipartition values) is opened at the end of the analysis in the default tree editor, if any.""")

    setP = Button(master, text='? ', command=info_open)  # ALIGNMENT FILE
    setP.grid(row=3, column=3, sticky=W, padx=2)
    setP.config(highlightbackground="light Grey")

    Label(master, text=' N. threads', bg="light Grey").grid(row=5, column=0, sticky=W)
    proc = IntVar()  # DEFINE NUMBER PROCESSORS
    opt2 = apply(OptionMenu, (master, proc) + tuple(listP[::1]))
    opt2.grid(row=5, column=1, sticky=W)
    opt2.config(bg="light Grey")
    proc.set(K[1])

    try:
        Nthr = "CPUs available: %s" % nthr
    except:
        Nthr = "CPUs available:"

        def proc_count():
            showerror("Warning", """Python module 'multiprocessing' not found! \n
The module can be downloaded at http://pypi.python.org/pypi/multiprocessing""")

        setP = Button(master, text='? ', command=proc_count)  # ALIGNMENT FILE
        setP.grid(row=5, column=3, sticky=W, padx=2)
        setP.config(highlightbackground="light Grey")

    if current_OS == 'MacOS' or current_OS == 'Linux':
        Label(master, text=Nthr, bg="light Grey").grid(row=5, column=2, sticky=E)

    Label(master, text=' Operating System', bg="light Grey").grid(row=4, column=0,
                                                                  sticky=W)  # DEFINE NUMBER BS REPLICATES
    OS = StringVar()
    opt5 = OptionMenu(master, OS, 'MacOS', 'Windows', 'Linux')
    opt5.grid(row=4, column=1, sticky=W, columnspan=2)
    opt5.config(bg="light Grey")
    OS.set(current_OS)
    # opt5.config(state=DISABLED)
    Term = StringVar()

    if current_OS == "MacOS":
        opt6 = OptionMenu(master, Term, 'Terminal', 'X11')
        opt6.grid(row=4, column=2, sticky=E, columnspan=2)
        opt6.config(bg="light Grey")
        # if current_OS != 'MacOS': opt6.config(state=DISABLED)
        Term.set(K[7])
    else:
        Term.set("Terminal")

    version = "%s" % K[0]
    Label(master, text=' RAxML version', bg="light Grey").grid(row=6, column=0, sticky=W)
    list_exe()
    Nthr = Button(master, text='+', command=raxmlV)

    if current_OS == "Windows":
        Nthr.grid(row=6, column=3, sticky=W, padx=2)
        Nthrd = Button(master, text='-', command=del_raxmlV, padx=2)
        Nthrd.grid(row=6, column=3)
    else:
        Nthr.grid(row=6, column=3, sticky=W)
        Nthrd = Button(master, text='-', command=del_raxmlV)
        Nthrd.grid(row=6, column=4, sticky=W)

    Nthr.config(highlightbackground="light Grey")
    Nthrd.config(highlightbackground="light Grey")
    ### SET CMD
    setR = Button(master, text='Defaults', pady=2, command=restore)  # ALIGNMENT FILE
    setR.grid(row=8, column=0, sticky=W)
    setR.config(highlightbackground="light Grey")
    Label(master, text='  ', bg="light Grey").grid(row=7, column=0, sticky=W)
    setC = Button(master, text='Cancel', pady=2, command=lambda: noset_pref(0))  # ALIGNMENT FILE
    setC.grid(row=8, column=1, sticky=E)
    setC.config(highlightbackground="light Grey")

    if current_OS == 'Windows':
        setC.config(highlightbackground="light Grey", padx=20)

    setB = Button(master, text='OK', padx=25, pady=2, command=lambda: set_pref(0), default=ACTIVE)  # ALIGNMENT FILE

    if current_OS == 'Windows':
        setB.grid(row=8, column=3, sticky=E)
    else:
        setB.grid(row=8, column=2, sticky=E)

    setB.config(highlightbackground="light Grey")
    master.bind("<Return>", set_pref)
    master.bind("<Escape>", noset_pref)

    if current_OS == 'MacOS':
        master.bind("<Command-w>", noset_pref)

#!/usr/bin/env python
# RAxMLGUI 0.9 build 20100519. Set options and run a fully custom RAxML analysis
# Created by Daniele Silvestro on 19/05/2010. => dsilvestro@senckenberg.de

import Tkinter
import csv
import os
import platform
import sys
from Tkinter import *
from os.path import expanduser
from tkFileDialog import *
from tkMessageBox import *

# self_path =os.path.join(os.path.split(__file__)[0]) # is the path of this file
self_path = os.getcwd()  # gives the path of this script if you run it from terminal
self_path = "%s/raxmlgui" % self_path
raxml_path = """ "%s/raxml" """ % self_path
setup_python_cipres_path = """ "%s/setup_python_cipres" """ % self_path


def install_python_cipres():
    if platform.system() == "Windows" or platform.system() == "Microsoft":
        runWin = "start /wait"
        winD = "/D"
    else:
        runWin = ""
        winD = ""
    # ans = askyesno("Install Python-CIPRES library", "A python_cipres library is required, do you want to install it?")
    # if ans:
    cmd = """cd %s %s && python setup.py install""" % (winD, setup_python_cipres_path)
    print "running:", cmd
    os.system(cmd)


def exc_panel():
    outfile = "%s/exc.txt" % self_path
    outfile = file(outfile, 'w')

    def sign_up_online():
        if platform.system() == "Darwin":
            cmd = """open https://www.phylo.org/restusers/register.action """
            os.system(cmd)
        elif platform.system() == "Windows" or platform.system() == "Microsoft":
            cmd = """ start https://www.phylo.org/restusers/register.action """
            os.system(cmd)
        else:
            cmd = """xdg-open https://www.phylo.org/restusers/register.action """
            os.system(cmd)

    def read_ID():
        try:
            home = expanduser("~")
            conf_file = "%s/pycipres.conf" % home
            f = open(conf_file, 'rb')
            L = f.readlines()
            usr = L[3].split("=")[1]
            pwd = L[4].split("=")[1]
            from_n.set(usr)
            to_n.set(pwd)
        except(IOError):
            showinfo("Warning", "No config file found!", parent=self)

    def erase_ID():
        home = expanduser("~")
        conf_file = "pycipres.conf"
        if platform.system() == "Windows" or platform.system() == "Microsoft":
            rm_conf_file = """cd "%s" && del "%s" """ % (home, conf_file)
        else:
            rm_conf_file = """cd '%s' && rm '%s' """ % (home, conf_file)

        print "CMD:", rm_conf_file
        ans = askyesno('Warning',
                       """This will permanently remove the 'pycipres.conf' file and associated information\n\nDo you want to continue?""",
                       parent=self)
        if ans: os.system(rm_conf_file)

    def write_ID():
        showinfo("Warning", """Your login information is saved in plain text in the file 'pycipres.conf' in your home folder.
Note, that anyone could run a job on CIPRES with your login while it is there. To remove permanently this information select the button 'Erase login data'.""",
                 parent=self)
        home = expanduser("~")
        conf_file = "%s/pycipres.conf" % home
        txt_conf = """URL=https://cipresrest.sdsc.edu/cipresrest/v1
APPNAME=raxmlGUI
APPID=raxmlGUI-E0684D0BA0A640098B305AA5CD60F4CD
USERNAME=%s
PASSWORD=%s""" % (from_n.get().strip(), to_n.get().strip())
##PASSWORD=%s""" % (from_n.get(), to_n.get())  ## Altered by Madhu to line above
        # print conf_file, txt_conf
        f = open(conf_file, 'wb')
        f.write(txt_conf)
        f.close()
        close("")

    def close(a):
        import main
        main.update_menu('exc_on')
        self.destroy()

    self = Toplevel()
    self.title("Set CIPRES login information")
    # self.geometry( "365x230" )
    # self.minsize(365,60)
    self.config(bg='light Grey')
    self.grab_set()
    if platform.system() == "Windows" or platform.system() == "Microsoft":
        icon = "%s/icon.ico" % self_path
        self.wm_iconbitmap(icon)
    a = Frame(self)
    a.pack(fill=X, expand=NO, side=TOP, anchor=W)
    a.config(bg="light Grey")
    b = Frame(self)
    b.pack(fill=X, expand=NO, side=TOP)
    b.config(bg="light Grey")
    c = Frame(self)
    c.pack(fill=X, expand=NO, side=TOP)
    c.config(bg="light Grey")
    # entry_1 FROM
    Label(a, text='  Username: ', bg="light Grey").pack(side=LEFT)
    from_n = StringVar()
    Label(a, text='   ', bg="light Grey").pack(side=RIGHT)
    entry1 = Entry(a, width=45, textvariable=from_n)
    entry1.pack(side=RIGHT)
    if platform.system() == "Darwin" or platform.system() == "Windows":
        entry1.config(font=(11), bg='white', fg='dark blue', highlightthickness=0)
    else:
        entry1.config(bg='white', fg='dark blue', highlightthickness=0)
    entry1.focus_set()
    # entry_2 TO
    Label(b, text='  Password: ', bg="light Grey").pack(side=LEFT)
    to_n = StringVar()
    Label(b, text='   ', bg="light Grey").pack(side=RIGHT)
    entry2 = Entry(b, width=45, textvariable=to_n)
    entry2.pack(side=RIGHT)
    if platform.system() == "Darwin" or platform.system() == "Windows":
        entry2.config(font=(11), bg='white', fg='dark blue', highlightthickness=0)
    else:
        entry2.config(bg='white', fg='dark blue', highlightthickness=0)

    button1 = Button(c, text='Save and close', padx=20, pady=2, command=write_ID)  # RUN RAXML
    button1.pack(side=RIGHT)
    button1.config(highlightbackground="light Grey")
    button2 = Button(c, text='Erase login data', padx=20, pady=2, command=erase_ID)  # RUN RAXML
    button2.pack(side=RIGHT)
    button2.config(highlightbackground="light Grey")
    button3 = Button(c, text='Show login data', padx=20, pady=2, command=read_ID)  # RUN RAXML
    button3.pack(side=RIGHT)
    button3.config(highlightbackground="light Grey")
    button4 = Button(c, text='Sign up', padx=20, pady=2, command=sign_up_online)  # RUN RAXML
    button4.pack(side=RIGHT)
    button4.config(highlightbackground="light Grey")

    # self.bind("<Return>", def_exc)
    self.bind("<Escape>", close)
    self.bind("<Command-w>", close)
    self.bind("<Control-w>", close)


    # exc_panel()

#!/usr/bin/env python2.6
# raxmlGUI 1.3.1 build 20141022. A graphical front-end for RAxML.
# Created by Daniele Silvestro and Ingo Michalak on 19/05/2010. 
# For bug reports and support contact raxmlGUI [dot] help [at] gmail [dot] com


import sys
import os #
import os.path
import platform
from Tkinter import * 
import Tkinter 
import csv
from tkMessageBox import *
from tkFileDialog import *

#self_path =os.path.join(os.path.split(__file__)[0]) # is the path of this file
self_path1 = os.getcwd()	# gives the path of this script if you run it from terminal	
self_path = "%s/raxmlgui" % self_path1
raxml_path = """ "%s/raxml" """% self_path
raxml_path_mod = "%s/raxml" % self_path

def log_file():
	log_f= "%s/raxmlGUI.log" % self_path1
	log_f = file(log_f, 'r')
	f = log_f.readlines()
	svname = asksaveasfilename(title="Save log file")
	if svname:
		sv_file = file(svname, 'w')
		for i in f:
			sv_file.write(i)
		sv_file.close()

def read_pref():
	global K, pref, current_OS, raxmlv, K
	pref = "%s/defaults" % self_path
	pref = file(pref, 'r')
	f = pref.readlines()  # DEFINING OUTGROUP
	K=list() # R[start:stop:step]
	j=0
	for i in f:
		param = i.split()
		if len(param) > 2:
			K.insert(j, param[1]+" "+param[2])     
		else:
			K.insert(j, param[1]) # the second is picked as parameter
		j=j+1
	raxmlv=K[0]
	
	current_OS = K[6]
	if K[6] == "MacOS" or K[6] == "Linux":
		K[0] = "./%s" % K[0]

def about():
	read_pref()
	raxmlGUIv="""   raxmlGUI v. 1.3.1"""
	message=    "Daniele Silvestro & Ingo Michalak"
	def more():
		more="""raxmlGUI 1.3.1 build 20141021\n\nContact: \nraxmlgui.help@gmail.com\n
\nraxmlGUI:\nSilvestro and Michalak (ODE, 2012)\nRAxML:\nStamatakis (Bioinformatics, 2014)"""
		showinfo("About raxmlGUI", more)
		self.destroy()
	#	grab.showinfo()
	def moore():
		self.minsize(360,485)
		self.maxsize(360,485)
		c = Frame(self)
		c.pack(fill=X, expand=NO, side=TOP)
		c.config(bg = "Grey", relief=FLAT)
		#t = Text(c, padx=80, pady=80, height=1)
		#m="iuhgfdsdfghbvc\nuhgvcxdfg"
		#t.insert(END, m)
	global gif
	self = Toplevel()
	self.title( "About raxmlGUI" )
	self.geometry( "365x270" )
	self.minsize(360,285)
	self.maxsize(360,285)
	self.config(bg='light Grey')
	self.grab_set()
	if platform.system() == "Windows" or platform.system() == "Microsoft":
		icon = "%s/icon.ico" % self_path
		self.wm_iconbitmap(icon)
		self.minsize(355,280)
		self.maxsize(355,280)
		
	a = Canvas(self, width = 500, height = 180, bg = "light Grey", relief=FLAT, highlightbackground="light Grey")
	a.pack(expand = NO, fill = NONE, side=TOP)
	gif1 = "%s/icon.gif" % self_path
	gif = PhotoImage(file = gif1)
	a.create_image(180, 90, image = gif)

	b = Frame(self)
	b.pack(fill=NONE, expand=NO, side=TOP)
	b.config(bg = "light Grey", relief=FLAT)

	texxt = Text(b, padx=80, pady=0, height=1)
	texxt.insert(END, raxmlGUIv)
	texxt.config(highlightthickness=0)                 
	texxt.pack(side=TOP, expand=NO, fill=NONE)
	if current_OS == "Windows" or current_OS == "Linux": texxt.config(font=('Arial', 15, 'bold'), relief=FLAT, bg='light Grey', fg= 'Black') 
	else: texxt.config(font=('Arial', 20, 'bold'), relief=FLAT, bg='light Grey', fg= 'Black') 
	texxt.config(state=DISABLED)

	c = Frame(self)
	c.pack(fill=X, expand=NO, side=TOP)
	c.config(bg = "light Grey", relief=FLAT)
	texxt1 = Text(c, padx=50, pady=0, height=2)
	texxt1.pack(side=TOP, expand=NO, fill=NONE)
	texxt1.config(highlightthickness=0)                 
	if current_OS == "Windows" or current_OS == "Linux": texxt1.config(font=('Arial', 12), relief=FLAT, bg='light Grey', fg= 'Black') 
	else: texxt1.config(font=('Arial', 14, 'bold'), relief=FLAT, bg='light Grey', fg= 'Black') 
	texxt1.insert(END, message)
	texxt1.config(state=DISABLED)
	button6 = Tkinter.Button(c, text='more...', padx=15, pady=2, command=more, default=ACTIVE)
	button6.pack(side=TOP)
	button6.config(highlightbackground =  "light Grey")
	def close_short(a): self.destroy()
	def more_short(a): more()
	self.bind("<Return>", more_short)
	self.bind("<Command-w>", close_short)	
	self.bind("<Control-w>", close_short)	
	self.bind("<Escape>", close_short)	

def helpraxml():
	read_pref()
	if current_OS=='MacOS':
		cmd= """open "%s/htmlhelp/help-RAxML.html" """% self_path # Help.pages
		os.system(cmd)
	if current_OS=='Linux':
		cmd= """xdg-open "%s/htmlhelp/help-RAxML.html" """% self_path # Help.pages
		os.system(cmd)
	if current_OS=='Windows':
		help_f =""" "" "%s/htmlhelp/help-RAxML.html" """% self_path
		cmd="start %s" % help_f
		os.system(cmd)
	
def help():
	read_pref()
	if current_OS=='MacOS':
		cmd= """open "%s/htmlhelp/help.pdf" """% self_path # Help.pages
		os.system(cmd)
	if current_OS=='Linux':
		cmd= """xdg-open "%s/htmlhelp/help.pdf" """% self_path # Help.pages
		os.system(cmd)
	if current_OS=='Windows':
		help_f =""" "" "%s/htmlhelp/help.pdf" """% self_path
		cmd="start %s" % help_f
		os.system(cmd)
	
def update():
	read_pref()
	if current_OS == 'MacOS':
		cmd= "open http://sourceforge.net/projects/raxmlgui/" 
		os.system(cmd)
	if current_OS=='Linux':
		cmd= "xdg-open http://sourceforge.net/projects/raxmlgui/" 
		os.system(cmd)
	if current_OS=='Windows':
		cmd= "start http://sourceforge.net/projects/raxmlgui/"
		os.system(cmd)

def updateraxml():
	read_pref()
	if current_OS == 'MacOS':
		cmd= "open https://github.com/stamatak/standard-RAxML" 
		os.system(cmd)
	if current_OS=='Linux':
		cmd= "xdg-open https://github.com/stamatak/standard-RAxML" 
		os.system(cmd)
	if current_OS=='Windows':
		cmd= "start https://github.com/stamatak/standard-RAxML" 
		os.system(cmd)
	
def joinmail():
	read_pref()
	if current_OS == 'MacOS':
		cmd= "open https://lists.sourceforge.net/lists/listinfo/raxmlgui-news" 
		os.system(cmd)
	if current_OS=='Linux':
		cmd= "xdg-open https://lists.sourceforge.net/lists/listinfo/raxmlgui-news" 
		os.system(cmd)
	if current_OS=='Windows':
		cmd= "start https://lists.sourceforge.net/lists/listinfo/raxmlgui-news" 
		os.system(cmd)

def export_citation(v):
	# export endnote
	if v==7: 
		exp_type="EndNote"
		filecontents = """<?xml version="1.0" encoding="UTF-8" ?><xml><records><record><ref-type name="Journal Article">17</ref-type><contributors><authors><author><style face="normal" font="default" size="100%">Silvestro, D.</style></author><author><style face="normal" font="default" size="100%">Michalak, I.</style></author></authors></contributors><titles><title><style face="normal" font="default" size="100%">raxmlGUI: a graphical front-end for RAxML</style></title></titles><periodical><full-title><style face="normal" font="default" size="100%">Organisms Diversity &amp; Evolution</style></full-title><abbr-1><style face="normal" font="default" size="100%">Org Divers Evol</style></abbr-1></periodical><pages><style face="normal" font="default" size="100%">DOI: 10.1007/s13127-011-0056-0</style></pages><dates><year><style face="normal" font="default" size="100%">2011</style></year></dates><urls><pdf-urls><url>http://dx.doi.org/10.1007/s13127-011-0056-0</url></pdf-urls></urls></record></records></xml>"""
	if v==8: 
		exp_type="RIS"
		filecontents = """
TY  - JOUR
ID  - 
A1  - Silvestro, D
A1  - Michalak, I
Y1  - 2011
JF  - Organisms Diversity & Evolution
JA  - Org Divers Evol
SN  - 
T1  - raxmlGUI: a graphical front-end for RAxML
M2  - 
M3  - 
SP  - 
EP  - 
L1  - 
L3  - 
ER  - 
DO  - 10.1007/s13127-011-0056-0
	"""
	if v==9: 
		exp_type="BibTeX"
		filecontents = """

@article{raxmlGUI,
author = {Daniele Silvestro and Ingo Michalak}, 
journal = {Organisms Diversity and Evolution},
title = {raxmlGUI: a graphical front-end for RAxML},
year = {2011},
DOI = {10.1007/s13127-011-0056-0},
}

	"""
	if v==10: 
		exp_type="txt"
		filecontents = "Silvestro, D. & Michalak, I. (2011) raxmlGUI: A graphical front-end for RAxML. Organisms Diversity & Evolution, DOI: 10.1007/s13127-011-0056-0"
	
	svname = asksaveasfilename(title="Export %s citation" % exp_type)
	if svname:
		sv_file = file(svname, 'w')
		sv_file.write(filecontents)		
		
		

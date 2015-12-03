#!/usr/bin/env python2.6
# raxmlGUI 1.0 build 20120121. A graphical front-end for RAxML.
# Created by Daniele Silvestro on 19/05/2010. => dsilvestro@senckenberg.de
# MULTIPLATFORM VERSION
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
	raxmlGUIv="""   raxmlGUI v. 1.5"""
	message=    "Daniele Silvestro & Ingo Michalak"
	def moore():
		more="""raxmlGUI 1.5 beta 20140615\n\nContact: \nraxmlgui.help@gmail.com\n
\nraxmlGUI:\nSilvestro and Michalak (Org Divers Evol, 2012)\nRAxML:\nStamatakis (Bioinformatics, 2006)
CIPRES-REST: Miller et al. (Evol Bioinform, 2015)"""
		showinfo("About raxmlGUI", more)
		self.destroy()
	#	grab.showinfo()
	def more():
				more="""
CONTACTS: \nraxmlgui.help@gmail.com
http://sourceforge.net/projects/raxmlgui/
\nREFERENCES:
raxmlGUI\nSilvestro and Michalak (Org Divers Evol, 2012)
RAxML\nStamatakis (Bioinformatics, 2014)
CIPRES-REST\nMiller et al. (Evol Bioinform, 2015)
\nACKNOWLEDGMENTS:
Thanks to Mark Miller and Terri Schwartz for the support 
integrating the CIPRES-REST services within raxmlGUI.
"""
				def close_cmd(a=0): 
					self_1.destroy()
					self.destroy()
				self_1 = Toplevel()
				self_1.title( "raxmlGUI 1.5 beta 20140424" )
				self_1.geometry( "450x200" )
				self_1.minsize(450,200)
				self_1.config(bg='light Grey')
				self_1.grab_set()
				if current_OS=='Windows':
					icon = "%s/icon.ico" % self_path
					self_1.wm_iconbitmap(icon)
				b = Frame(self_1, relief=RAISED, borderwidth=1)
				b.pack(fill=X, expand=NO, side=BOTTOM)
				b.config(bg = "light Grey")
				Label(b, text='  ', bg = "light Grey").pack(side=RIGHT)
				setA = Button(b, text='Close', padx=25, pady=2 , command=close_cmd) #
				setA.pack(side=RIGHT)
				setA.config(highlightbackground = "light Grey")
				texxt_1 = Text(self_1, padx=35, pady=0, width=20, height=10)
				texxt_1.pack(side=TOP, expand=NO)#, fill=Y)
				texxt_1.config(highlightthickness=0)                 
				sbar = Scrollbar(self_1)
				sbar.config(command=texxt_1.yview)                   
				texxt_1.config(yscrollcommand=sbar.set)
				sbar.pack(fill=Y, expand=YES)                                   
				if current_OS=='MacOS' or current_OS=='Windows': texxt_1.config(relief=GROOVE, bg='#e6e6e6', fg= 'dark blue', font=(11), state=DISABLED)
				else: texxt_1.config(relief=GROOVE, bg='#e6e6e6', fg= 'dark blue', font=(10), state=DISABLED)
				texxt_1.pack(side=LEFT, expand=YES, fill=BOTH)
				texxt_1.config(state=NORMAL)
				texxt_1.insert(END, more)
				texxt_1.config(state=DISABLED)
				self_1.bind("<Escape>", close_cmd)
				self_1.bind("<Command-w>", close_cmd)
				if current_OS=='Windows': self_1.bind("<Control-w>", close_cmd)			
				
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
		
def beta_info(current_OS):
	detailed_msg = """This is a beta version! 

This version of raxmlGUI you can run your analyses (currently with limited
functions) using the CIPRES Science Gateway (Miller et al. 2011) via the
REST API (Miller et al. 2015). You will need to install the necessary
python toolkit, kindly provided by Terri Schwartz from the SDSC and
included in the package.

Further details are provided in the updated manual. For additional info,
suggestions, bug reports please contact us at raxmlgui.help@gmail.com.
You can download previous stable versions orf raxmlGUI at
http://sourceforge.net/projects/raxmlgui/files/.

"""
	self_1 = Toplevel()
	try: self_1.wm_attributes('-topmost', 1)
	except: pass
	self_1.title( "raxmlGUI 1.5 beta 1" )
	self_1.geometry( "565x230" )
	self_1.minsize(565,230)
	self_1.config(bg='light Grey')
	self_1.grab_set()
	if current_OS=='Windows':
		icon = "%s/icon.ico" % self_path
		self_1.wm_iconbitmap(icon)
	b = Frame(self_1, relief=RAISED, borderwidth=1)
	b.pack(fill=X, expand=NO, side=BOTTOM)
	b.config(bg = "light Grey")
	Label(b, text='  ', bg = "light Grey").pack(side=RIGHT)
	setA = Button(b, text='Close', padx=25, pady=2 , command=self_1.destroy) #
	setA.pack(side=RIGHT)
	setA.config(highlightbackground = "light Grey")
	texxt_1 = Text(self_1, padx=35, pady=0, width=20, height=10)
	texxt_1.pack(side=TOP, expand=NO)#, fill=Y)
	texxt_1.config(highlightthickness=0)                 
	sbar = Scrollbar(self_1)
	sbar.config(command=texxt_1.yview)                   
	texxt_1.config(yscrollcommand=sbar.set)
	sbar.pack(fill=Y, expand=YES)                                   
	if current_OS=='MacOS' or current_OS=='Windows': texxt_1.config(relief=GROOVE, bg='#e6e6e6', fg= 'dark blue', font=(15), state=DISABLED)
	else: texxt_1.config(relief=GROOVE, bg='#e6e6e6', fg= 'dark blue', font=('Monaco', 12), state=DISABLED)
	texxt_1.pack(side=LEFT, expand=YES, fill=BOTH)
	texxt_1.config(state=NORMAL)
	texxt_1.insert(END, detailed_msg)
	texxt_1.config(state=DISABLED)
	def close_cmd(a): self_1.destroy()
	self_1.bind("<Escape>", close_cmd)
	self_1.bind("<Command-w>", close_cmd)
	if current_OS=='Windows': self_1.bind("<Control-w>", close_cmd)	

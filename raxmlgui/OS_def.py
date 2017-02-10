#!/usr/bin/env python2.6
# RAxMLGUI 0.9 build 20100519. Set options and run a fully custom RAxML analysis
# Created by Daniele Silvestro on 20/01/2010. => dsilvestro@senckenberg.de

import sys
import os
from Tkinter import * 
import Tkinter 
import csv
import platform
from tkMessageBox import *
from tkFileDialog import *

#self_path =os.path.join(os.path.split(__file__)[0]) # is the path of this file
self_path = os.getcwd()	# gives the path of this script if you run it from terminal	
self_path = "%s/raxmlgui" % self_path
raxml_path = """ "%s/raxml" """% self_path
pref = "%s/defaults" % self_path
pref = file(pref, 'r')

def parse_all():
	f = pref.readlines()  # DEFINING OUTGROUP
	global K
	K=list() # R[start:stop:step]
	j=0
	print f
	for i in f:
		param = i.split()
		if len(param) > 2:
			K.insert(j, param[1]+" "+param[2])     
		else:
			K.insert(j, param[1]) # the second is picked as parameter
		j=j+1
	global detectedOS
	detectedOS=K[6]

try: parse_all()
except:
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
	parse_all()


def setOSauto():
	print detectedOS
	if detectedOS == 'MacOS' or detectedOS == 'Windows' or detectedOS == 'Linux':
		if detectedOS == 'Windows': binary = "_8121.exe"
		if detectedOS == 'MacOS': binary = "-SSE3-Mac"
		if detectedOS == 'Linux': binary = "_8121_Ubuntu"
		
		outfile = "%s/defaults" % self_path
		outfile = file(outfile, 'w')
		pref = "%s/defaults" % self_path
		pref = file(pref, 'r')
		try: 
			import multiprocessing
			nthr = multiprocessing.cpu_count()
			if nthr>2:
				if detectedOS == 'MacOS': binary = "-PTHREADS-SSE3-Mac"
				if detectedOS == 'Windows': binary = "-PTHREADS-SSE3_8121.exe"
		except: pass
		pref_def = """RAxML_version: raxmlHPC%s
Number_processors: %s 
Substitution_Model: %s 
Analysis: %s 
BS_replicates: %s 
open_MLtree: %s
OS: %s
Term: Terminal
Toolbar_color: DBDBDB
Wrap_line: none""" % (binary, K[1], K[2], K[3], K[4], K[5], detectedOS)
		outfile.writelines(pref_def)
		outfile.close()
	
def defOS():
	def warn():
		showinfo("", "Please restart raxmlGUI to make the changes effective!") 
	def set_OS():
		outfile = "%s/defaults" % self_path
		outfile = file(outfile, 'w')
		pref = "%s/defaults" % self_path
		pref = file(pref, 'r')
		pref_def = """RAxML_version: raxmlHPC-%s 
Number_processors: %s 
Substitution_Model: %s 
Analysis: %s 
BS_replicates: %s 
open_MLtree: %s
OS: %s
Term: Terminal
Toolbar_color: DBDBDB
Wrap_line: none""" % (OS.get(), K[1], K[2], K[3], K[4], K[5], OS.get())
		outfile.writelines(pref_def)
		warn()
		
######
	self = Toplevel()
	self.title( "Select OS" )
	self.geometry( "400x87" )
	self.config(bg='light Grey')
 
	tool = Frame(self, relief=FLAT, borderwidth=1)
	tool.pack(fill=X, expand=NO, side=TOP)
	tool.config(bg = "light Grey")
	Label(tool, text='Please select the current operating system:', bg = "light Grey").pack(side=TOP)	
	Label(tool, text='(the default OS can be changed from the Preferences panel)', bg = "light Grey").pack(side=TOP)
	a = Frame(self, relief=FLAT)
	a.pack(fill=NONE, expand=NO, side=TOP)
	a.config(bg = "light Grey")
	setB = Button(a, text='Set', padx=25, pady=2, command=set_OS)
	setB.pack(side=RIGHT)
	setB.config(highlightbackground = "light Grey")
	OS = StringVar()
	opt4 = OptionMenu(a, OS,'MacOS', 'Windows', 'Linux') 
	opt4.pack(side=RIGHT)
	OS.set(detectedOS)
	opt4.config(bg = "light Grey")

#####
if platform.system() == "Darwin":
	detectedOS = 'MacOS'
	setOSauto()
elif platform.system() == "Windows" or platform.system() == "Microsoft":
	detectedOS = 'Windows'
	setOSauto()
elif platform.system() == "Linux":
	detectedOS = 'Linux'	
	setOSauto()
else: defOS()
	
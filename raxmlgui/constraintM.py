#!/usr/bin/env python2.6
# raxmlGUI 1.3.1 build 20141022. A graphical front-end for RAxML.
# Created by Daniele Silvestro and Ingo Michalak on 19/05/2010. 
# For bug reports and support contact raxmlGUI [dot] help [at] gmail [dot] com

import sys
import os
import platform
from Tkinter import * 
import Tkinter 
import csv
from tkColorChooser import askcolor
from tkMessageBox import *
from tkFileDialog import *
# MULTI-PLATFORM
#self_path =os.path.join(os.path.split(__file__)[0]) # is the path of this file
self_path = os.getcwd()	# gives the path of this script if you run it from terminal	
#print "\n\t", self_path, "\n"
self_path = "%s/raxmlgui" % self_path
raxml_path = """ "%s/raxml" """% self_path

		
def listTaxa(taxaL, out_con):
	def set_out():
		showinfo("Warning", "If the outgroups are not monophyletic,\
 the first name in the list will be selected as outgroup!", parent=master)
		tree= listbox2.get(0, END)
		treeT = ",".join(tree)
		print treeT
		import main
		main.out(treeT)
		master.destroy()

	def set_con():
		global taxset, export, constr
		list_con=add_con()
		pref = "%s/constraint.tre" % self_path
		pref = file(pref, 'w')
		treeT = ", ".join(list(list_con))
		if constr.get()=='yes':
			#if taxset>1: treeT="(%s);" % treeT
			tree= listbox1.get(0, END)
			clade = ", ".join(tree)
			treeT = "%s, %s" % (treeT, clade)


		if taxset>1 or constr.get()=='yes': treeT="(%s);" % treeT
		else: treeT="%s;" % treeT
		pref.writelines(treeT)
		print treeT
		if export.get()=="yes":
			svname = asksaveasfilename(title="Save multifurcating tree constraint")
			if svname:
				sv_file = file(svname, 'w')
				sv_file.write(treeT)
				sv_file.close()
		import main
		main.constraint('5')
		master.destroy()

	def add_con():
		tree= listbox2.get(0, END)
		clade = ", ".join(tree)
		clade="(%s)" % clade
		if clade=="()": pass
		else: 
			global taxset
			taxset=taxset+1
			if taxset==1: label="1 constraint enforced"
			else: label="%s constraints enforced" % taxset
			Label(master, text=label, bg = "light Grey").grid(row=3,  column=1, sticky=E, columnspan=2)
			list_con.append(clade)
			listbox2.delete(0, END)
			print list_con
			setA.config(state=DISABLED)
		return list_con
		
	def include():
		included=listbox1.curselection()
		#print included
		i=0
		for item in included: 
			item=int(item)
			listbox2.insert(END, (listbox1.get(item+i)))# taxaL[item])
			listbox1.delete(item+i) #taxaL[item], taxaL[item])
			i=i-1
		try: setA.config(state=NORMAL)
		except: pass
		if out_con=='constraint': 
			def short_add(a): add_con()
			setA.config(state=NORMAL, default=ACTIVE)
			setB.config(state=NORMAL)
			master.bind("<Return>", short_add)
		else:
			def short_out(a): set_out()
			setB.config(state=NORMAL, default=ACTIVE)
			master.bind("<Return>", short_out)
	def exclude():
		excluded=listbox2.curselection()
		#print excluded
		i=0
		for item in excluded: 
			item=int(item)
			listbox1.insert(END, (listbox2.get(item+i)))
			listbox2.delete(item+i) #taxaL[item], taxaL[item])
			i=i-1
	
	def reset_close(): 
		global taxset
		tree= listbox2.get(0, END)
		if len(tree)==0 and taxset<=0: master.destroy()
		else: 
			ans = askyesno("Save settings", "Do you want to save the current settings?", parent=master)
			if ans: 
				try: set_con()
				except: set_out()
			else: master.destroy()
######
	master = Toplevel()
	master.protocol("WM_DELETE_WINDOW", reset_close)
	if out_con=='constraint': master.title( "Taxa constraint" )
	else: master.title( "Multiple outgroup" )
#	master.geometry( "550,435" )
	master.config(bg='light Grey')
	if platform.system() == "Windows" or platform.system() == "Microsoft":
		icon = "%s/icon.ico" % self_path
		master.wm_iconbitmap(icon) 
		master.minsize(420,400)
		#master.maxsize(320,235)
	else:
		master.minsize(650,435)
		#master.maxsize(550,435)
	def short_close(a): reset_close()
	master.bind("<Command-w>", short_close)
	master.bind("<Control-w>", short_close)
	master.grab_set()

	global taxset
	taxset =0 
	list_con=list()
	if out_con=='constraint': label=' Taxa'
	else: label='  Ingroup'
	Label(master, text="  ", bg = "light Grey").grid(row=0,  column=0, sticky=W)
	Label(master, text=label, bg = "light Grey").grid(row=0,  column=1, sticky=W)
	sel_taxa = list()
	listbox1 = Listbox(master, selectmode=EXTENDED, listvariable=sel_taxa, width=30, height=20) #MULTIPLE)
	listbox1.grid(row=1,  column=1, sticky=W, rowspan=2)
	sbar = Scrollbar(master, orient=VERTICAL)
	sbar.config(command=listbox1.yview)
	listbox1.config(yscrollcommand=sbar.set)
	sbar.grid(row=1,  column=1, sticky=N+S+E, rowspan=2)
	for item in range(2, len(taxaL)): listbox1.insert(END, taxaL[item])

	if out_con=='constraint': label=' Constrained taxa'
	else: label=' Outgroup'
	Label(master, text=label, bg = "light Grey").grid(row=0,  column=3, sticky=W)
	replicate = list()
	listbox2 = Listbox(master, selectmode=EXTENDED, width=30, height=20) #EXTENDED)
	listbox2.grid(row=1,  column=3, sticky=W, rowspan=2)
	sbar = Scrollbar(master, orient=VERTICAL)
	sbar.config(command=listbox2.yview)
	listbox2.config(yscrollcommand=sbar.set)
	sbar.grid(row=1,  column=3, sticky=N+S+E, rowspan=2)
	
	
	inclB = Button(master, text='->', command=include) # ALIGNMENT FILE
	inclB.grid(row=1,  column=2, sticky=W, padx=2)	
	inclB.config(highlightbackground = "light Grey")

	inclB = Button(master, text='<-', command=exclude) # ALIGNMENT FILE
	inclB.grid(row=2,  column=2, sticky=W, padx=2)	
	inclB.config(highlightbackground = "light Grey")
	label=	"To select more than one taxon hold shift or ctrl."
	Label(master, text=label, bg = "light Grey").grid(row=4,  column=1, sticky=W, columnspan=4)

	if out_con=='constraint':
		setA = Button(master, text='Add   ', command=add_con) # ALIGNMENT FILE
		setA.grid(row=3,  column=1, sticky=W, padx=2, columnspan=2)	
		setA.config(highlightbackground = "light Grey", state=DISABLED)
		setC = Button(master, text='Cancel', command=master.destroy) # ALIGNMENT FILE
		setC.grid(row=5,  column=3, padx=2, columnspan=2)	
		setC.config(highlightbackground = "light Grey", state=NORMAL)
		setB = Button(master, text='OK   ', command=set_con) # ALIGNMENT FILE
		setB.grid(row=5,  column=3, padx=2, columnspan=2, sticky=E)	
		setB.config(highlightbackground = "light Grey", state=DISABLED)
		global export, constr
		export= StringVar()
		setD = Checkbutton(master, text='Export constraint...', variable=export, onvalue="yes", offvalue="no") # ALIGNMENT FILE
		setD.grid(row=3,  column=3, padx=2, columnspan=1, sticky=W)	
		setD.config(bg = "light Grey", state=NORMAL)
		setD.deselect()

		constr= StringVar()
		setE = Checkbutton(master, text='Monophyletic contraints', variable=constr, onvalue="yes", offvalue="no") # ALIGNMENT FILE
		setE.grid(row=4,  column=3, padx=2, columnspan=1, sticky=W)	
		setE.config(bg = "light Grey", state=NORMAL)
		setE.deselect()

		Label(master, text="0 constraint enforced", bg = "light Grey").grid(row=3,  column=1, sticky=E, columnspan=2)
	else:
		setB = Button(master, text='Set as outgroup', command=set_out) # ALIGNMENT FILE
		setB.grid(row=3,  column=3, sticky=E, padx=2)	
		setB.config(highlightbackground = "light Grey", state=DISABLED)

		setC = Button(master, text='Cancel', command=master.destroy) # ALIGNMENT FILE
		setC.grid(row=3,  column=3, padx=2, sticky=W, columnspan=2)	
		setC.config(highlightbackground = "light Grey", state=NORMAL)

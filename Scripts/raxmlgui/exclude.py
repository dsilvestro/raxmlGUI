#!/usr/bin/env python2.6
# RAxMLGUI 0.9 build 20100519. Set options and run a fully custom RAxML analysis
# Created by Daniele Silvestro on 19/05/2010. => dsilvestro@senckenberg.de

import sys
import os
import platform
from Tkinter import * 
import Tkinter 
import csv
from tkMessageBox import *
from tkFileDialog import *

#self_path =os.path.join(os.path.split(__file__)[0]) # is the path of this file
self_path = os.getcwd()	# gives the path of this script if you run it from terminal	
self_path = "%s/raxmlgui" % self_path
raxml_path = """ '%s/raxml' """% self_path 

def exc_start():
	global maxchar, Mdtype, setA
	outfile = "%s/exc.txt" % self_path #deletes old partition 
	outfile = file(outfile, 'r')
	maxchar= outfile.readlines()
	maxchar = maxchar[0]
	outfile.close()
	exc_panel()



def exc_panel():
	outfile = "%s/exc.txt" % self_path
	outfile = file(outfile, 'w')
	def set_exc():
		All_part = texxt.get(1.0, END)
		outfile.writelines(All_part)
		outfile.close()
		import main
		main.update_menu('exc_on')
		main.exc()		
		self.destroy()
	def del_exc():
		showerror("Error", "wait wait")
		self.destroy()
	def def_exc(a):
		try:
			if int(to_n.get()) >= int(from_n.get()) and int(from_n.get()) > 0 and int(to_n.get()) <= int(maxchar):
				exc_str= "%s-%s\n" % (from_n.get(), to_n.get())
		#		print int(to_n.get()), int(from_n.get()), maxchar
				texxt.config(state=NORMAL)
				texxt.insert(END, exc_str)
				texxt.config(state=DISABLED)
				setA.config(state=NORMAL)
				setB.focus_set()	
			else:
				raise ValueError()
		except ValueError:
			err = "Illegal entry! Please enter an integer number to exclude characters. The numbers must be in range %s-%s." % (1, maxchar)
			showerror("llegal entry!", err)

	def edit_part():
		texxt.config(state=NORMAL)
		setA.config(state=NORMAL)
		texxt.focus_set()

	def export():
		svname = asksaveasfilename(title="Save exclusion-sites file")
		if svname:
			filecontents = texxt.get(1.0, END)
			sv_file = file(svname, 'w')
			sv_file.write(filecontents)
	def import_f():
		(fileinputS) = askopenfilename(title="Import exclusion-sites file")
		if	fileinputS:
			s = file(fileinputS,'U')
			lines = file(fileinputS,'U').read()  # lines = s.readlines()
			texxt.config(state=NORMAL)
			texxt.delete("1.0", END)
			texxt.insert(END, lines)
			texxt.config(state=DISABLED)
			setA.config(state=NORMAL)
	def close(a): 
		import main
		main.update_menu('exc_on')
		self.destroy()
	
	self = Toplevel()
	self.title( "Exclude sites" )
	self.geometry( "365x230" )
	self.minsize(365,230)
	self.config(bg='light Grey')
	self.grab_set()
	if platform.system() == "Windows" or platform.system() == "Microsoft":
		icon = "%s/icon.ico" % self_path
		self.wm_iconbitmap(icon) 
	a = Frame(self, relief=GROOVE, borderwidth=1)
	a.pack(fill=X, expand=NO, side=TOP, anchor=W)
	a.config(bg = "light Grey")
	b = Frame(self, relief=RAISED, borderwidth=1)
	b.pack(fill=X, expand=NO, side=BOTTOM)
	b.config(bg = "light Grey")
	# entry_1 FROM
	Label(a, text='   from ', bg = "light Grey").pack(side=LEFT)
	from_n = IntVar()
	entry1 = Entry(a, width = 6, textvariable = from_n)
	entry1.pack(side=LEFT)
	if platform.system() == "Darwin" or platform.system() == "Windows":
		entry1.config(font=(11), bg='white', fg= 'dark blue', highlightthickness=0)  
	else: entry1.config(bg='white', fg= 'dark blue', highlightthickness=0)  
	entry1.focus_set()	
	# entry_2 TO
	Label(a, text=' to ', bg = "light Grey").pack(side=LEFT)
	to_n = IntVar()
	entry2 = Entry(a, width = 6, textvariable = to_n)
	entry2.pack(side=LEFT)
	if platform.system() == "Darwin" or platform.system() == "Windows":
		entry2.config(font=(11), bg='white', fg= 'dark blue', highlightthickness=0)  
	else:
		entry2.config(bg='white', fg= 'dark blue', highlightthickness=0)  
	Label(a, text=' ', bg = "light Grey", font=('Times', 30)).pack(side=LEFT)
	setB = Button(a, text='OK', padx=25, pady=2, command=lambda: def_exc(0))#, default=ACTIVE) #
	setB.pack(side=RIGHT)
	setB.config(highlightbackground = "light Grey", state=NORMAL, default=ACTIVE)
	status= " %s characters" % (maxchar)
	Label(b, text=status, bg = "light Grey", fg= 'dark blue').pack(side=LEFT)
	if platform.system() == "Darwin":
		Label(b, text='  ', bg = "light Grey").pack(side=RIGHT)
	mbutton = Menubutton(b, text='Options') #, padx=16)
	mbutton.pack(side=RIGHT)
	picks = Menu(mbutton)               
	mbutton.config(menu=picks, bg ="light Grey", relief=RAISED)
	picks.add_command(label='Edit exclusion sites', command=edit_part)	
	picks.add_command(label='Import exclusion sites file...', command=import_f)
	picks.add_command(label='Export exclusion sites file...', command=export)	
	picks.add_command(label='Reset exclusion sites and close...', command=lambda: close(0))
	setA = Button(b, text='Set', padx=25, pady=2 , command=set_exc) #
	setA.pack(side=RIGHT)
	setA.config(highlightbackground = "light Grey", state=DISABLED)

	texxt = Text(self, padx=35, pady=0, width=20, height=10)
	texxt.pack(side=TOP, expand=NO)#, fill=Y)
	texxt.config(highlightthickness=0)                 
	sbar = Scrollbar(self)
	sbar.config(command=texxt.yview)                   
	texxt.config(yscrollcommand=sbar.set)
	sbar.pack(fill=Y, expand=YES)                                   
	if platform.system() == "Darwin" or platform.system() == "Windows": texxt.config(relief=GROOVE, bg='#e6e6e6', fg= 'dark blue', font=(11), state=DISABLED)
	else: texxt.config(relief=GROOVE, bg='#e6e6e6', fg= 'dark blue', font=('Monaco', 10), state=DISABLED)
	texxt.pack(side=LEFT, expand=YES, fill=BOTH)
	self.bind("<Return>", def_exc)
	self.bind("<Escape>", close)
	self.bind("<Command-w>", close)
	self.bind("<Control-w>", close)

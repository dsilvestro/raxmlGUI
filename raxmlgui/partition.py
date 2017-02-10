#!/usr/bin/env python2.6
# raxmlGUI 0.93 build 20100730. A graphical front-end for RAxML.
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

def part_start():
	global maxchar, Mdtype, editmode, P_list, statusMdtype
	outfile = "%s/info.txt" % self_path 
	outfile = file(outfile, 'U')
	maxchar= outfile.readlines()
	statusMdtype=  str(maxchar[1])
	if statusMdtype=="MIXED":
		Mdtype="DNA"
	else:
		Mdtype=statusMdtype
	maxchar = int(maxchar[0])
	editmode="No"
	outfile.close()
	part()

def reset_close_main():
	global num, nP, outfile, from_n, part_name
	print 
#	setB.config(state=NORMAL)
	num=nP=0
	outfile = "%s/part.txt" % self_path
	outfile = file(outfile, 'w')
	pref_def = " " 
	outfile.writelines(pref_def)
	editmode="No"

def part_edit():
	global editmode, P_list, maxchar, Mdtype, statusMdtype
	outfile = "%s/info.txt" % self_path #deletes old partition settings
	outfile = file(outfile, 'U')
	maxchar= outfile.readlines()
	statusMdtype=  str(maxchar[1])
	maxchar = int(maxchar[0])
	outfile = "%s/part.txt" % self_path 
	outfile = file(outfile, 'U')
	P_list = outfile.readlines()
	i=0
#	for line in P_list:
#		if line.strip(): del line
	statusMdtype="partitioned"# % len(P_list)
#	statusMdtype="%s partitions" % len(P_list)
	Mdtype="DNA"
	editmode="Yes"
	part()

def export():
	outfile = "%s/info.txt" % self_path #deletes old partition settings
	outfile = file(outfile, 'U')
	maxchar= outfile.readlines()
	statusMdtype=  str(maxchar[1])
	maxchar = int(maxchar[0])
	outfile = "%s/part.txt" % self_path 
	outfile = file(outfile, 'U')
	P_list = outfile.readlines()
	svname = asksaveasfilename(title="Save partition file")
	if svname:
		sv_file = file(svname, 'w')
		for i in range(0, len(P_list)):
			filecontents = "%s" % P_list[i] #texxt.get(1.0, END)
			sv_file.write(filecontents)
		
num=nP=0
def part():
	def destroy_w(ans):
		import main
		if ans=='n': main.update_menu('part_on')
		else: main.update_menu('set_part')
		self.destroy()

	global outfile, nP, num, to_n, from_n, part_name, data_type, data_typeAA, a, tool, labels, maxchar, editmode, P_list, statusMdtype
	outfile = "%s/part.txt" % self_path
	outfile = file(outfile, 'w')
	nP= num= to_n= from_n= 0
	def set_part():
		All_part = texxt.get(1.0, END)
		outfile.writelines(All_part)
		outfile.close()
		import main
		arg =""" -q "%s/part.txt" """% self_path
		main.check_seq(arg)
		destroy_w('y')
		main.apply_part_brL()
		
	def end():
		setB.config(state=DISABLED)
		ans = askokcancel("Partitioning completed", "All characters have been assigned to partitions.\nSet partitions for the analysis?", parent=self)
		if ans: set_part()
		else: edit_part()

	def def_part():
		try:
			global nP, num, to_n, from_n, part_name, data_type, data_typeAA, All_part, a, tool, data_typeF, tool2, data_typeDNA, Imodel, maxchar
			nP=nP+1
			num=num+1
			if num > 1: #try:  #
				dtype = data_type.get()
				if dtype == 'AA':
					data_typeF = "%s%s" % (data_typeAA.get(), Imodel.get())
				else:
					data_typeF = "%s" % data_type.get()
				line = "\n%s,\t %s = %s-%s" % (data_typeF, part_name.get(), from_n.get(), to_n.get())
				# DNA
				if dtype == 'DNA':
					if data_typeDNA.get() == 'codon specific':
						line = """\n%s,\t %s_codon1 = %s-%s\%s \n%s,\t %s_codon2 = %s-%s\%s \n%s,\t %s_codon3 = %s-%s\%s""" \
						% (data_typeF, part_name.get(), from_n.get(), to_n.get(), "3", \
						   data_typeF, part_name.get(), (int(from_n.get())+1), to_n.get(),  "3",\
						   data_typeF, part_name.get(), (int(from_n.get())+2), to_n.get(), "3")
					if data_typeDNA.get() == '3rd codon':
						line = """\n%s,\t %s_codon1and2 = %s-%s\%s, %s-%s\%s \n%s,\t %s_codon3 = %s-%s\%s""" \
						% (data_typeF, part_name.get(), from_n.get(), to_n.get(), "3", \
							(int(from_n.get())+1), to_n.get(),  "3",\
						   data_typeF, part_name.get(), (int(from_n.get())+2), to_n.get(), "3")
					
				num= to_n.get()+1
				if to_n.get() < int(from_n.get()) or to_n.get() > maxchar:
		#			print "TO_N:", to_n.get(), from_n.get(), to_n.get()-int(from_n.get())
					raise(ValueError)
				a = from_n.get(), to_n.get()
				texxt.config(state=NORMAL)
				texxt.insert(END, line)
				if editmode is not "Yes":
					texxt.config(state=DISABLED)
				try: All_part= All_part + a					
				except: All_part=a

			texxt.see(END)
			try: tool2.destroy()
			except: pass

			def model(value, args=None):
				global data_typeAA, labels, data_type, data_typeDNA, toolM, Imodel
				 
				try: toolM.destroy()
				except: pass 
				Label(self, text="  Model", bg = "light Grey").grid(row=0,  column=4, sticky=W, columnspan=2)

				toolM = Frame(self)
				toolM.grid(row=1,  column=4, sticky=W)#, columnspan=2)
				toolM.config(bg = "light Grey")

				if data_type.get() == 'AA':
					data_typeAA = StringVar()
					opt4 = OptionMenu(toolM, data_typeAA, 'DAYHOFF', 'DCMUT', 'JTT', 'MTREV', 'WAG', 'RTREV', 'CPREV', 'VT', 'BLOSUM62', 'MTMAM', 'LG', 'GTR', 'MTART', 'MTZOA', 'PMB', 'HIVB', 'HIVW', 'JTTDCMUT', 'FLU')
					opt4.grid(row=1,  column=4, sticky=W)
					opt4.config(bg = "light Grey",width=len('JTTDCMUT')+3)#, width =7)
					data_typeAA.set('DAYHOFF')
					Imodel = StringVar()
					check1 = Checkbutton(toolM, text="Emp. Freq.", variable=Imodel, onvalue="F", offvalue=" ")
					check1.config(bg = "light Grey")
					check1.grid(row=1,  column=5, sticky=E)
					check1.deselect()
					#self.minsize(540,230)	 
				if data_type.get() == 'DNA':
					data_typeDNA = StringVar()
					opt4 = OptionMenu(toolM, data_typeDNA, 'no codon', 'codon specific', '3rd codon') 
					opt4.grid(row=1,  column=4, sticky=W, columnspan=2)
					opt4.config(bg = "light Grey",width=len('codon_specific')+3)#, width =10)
					data_typeDNA.set('no codon')
				if data_type.get() == 'BIN' or data_type.get() == 'MULTI': #print data_type.get()
					try: toolM.destroy()
					except: pass
					Label(self, text="  ", bg = "light Grey").grid(row=0,  column=4, sticky=W+E, columnspan=2)
						
			tool2 = Frame(tool)
			tool2.grid(row=1,  column=0, sticky=W)
			tool2.config(bg = "light Grey")
			data_type = StringVar()
		#	Label(tool2, text=' ', bg = "light Grey").pack(side=LEFT)
			opt4 = OptionMenu(self, data_type,'DNA', 'BIN', 'MULTI', 'AA', command=model)
			opt4.grid(row=1,  column=0, sticky=W)
			opt4.config(bg = "light Grey", width =8)
			
			data_type.set(Mdtype)
			# PART NAME
			part_name = StringVar()
			entry = Entry(self, width = 11, textvariable = part_name)
			entry.grid(row=1,  column=1, sticky=W)
			if platform.system() == "Darwin" or platform.system() == "Windows":
				entry.config(font=(11), bg='white', fg= 'dark blue', highlightthickness=0)  
			else:
				entry.config(bg='white', fg= 'dark blue', highlightthickness=0)  
			name= "part_%s" % nP
			part_name.set(name)
			
			# FROM
	#		Label(tool2, text='  ', bg = "light Grey").pack(side=LEFT)
			from_n = StringVar()
			entry = Entry(self, width = 5, textvariable = from_n)
			entry.grid(row=1,  column=2, sticky=W)
			if platform.system() == "Darwin" or platform.system() == "Windows":
				entry.config(font=(11), bg='white', fg= 'dark blue', highlightthickness=0)  
			else:
				entry.config(bg='white', fg= 'dark blue', highlightthickness=0)  
			from_n.set(num)
			if editmode is not "Yes": entry.config(state=DISABLED)
			
			# TO
		#	Label(tool2, text=' ', bg = "light Grey").pack(side=LEFT)
			to_n = IntVar()
			entry = Entry(self, width = 5, textvariable = to_n)
			entry.grid(row=1,  column=3, sticky=W)
			if platform.system() == "Darwin" or platform.system() == "Windows":
				entry.config(font=(11), bg='white', fg= 'dark blue', highlightthickness=0)  
			else:
				entry.config(bg='white', fg= 'dark blue', highlightthickness=0)  
			entry.focus_set()
			model('DNA')
			to_n.set(num)
			if num >= maxchar:
				end()
		except (ValueError):
			err = "Illegal entry! Please enter an integer number to define a partition. The number must be in range %s-%s" % (from_n.get(), maxchar)
			showerror("Error", err, parent=self)
			nP=nP-1
			print All_part			
		
	def undo_part():
		global num, nP, outfile, from_n, part_name
		setB.config(state=NORMAL)
		num=nP=0
		texxt.config(state=NORMAL)
		texxt.delete(1.0, END)
		texxt.config(state=DISABLED)
		outfile.close()
		outfile = "%s/part.txt" % self_path
		outfile = file(outfile, 'w')
		pref_def = " " 
		outfile.writelines(pref_def)
		from_n.set(1)
		to_n.set(1)
		part_name.set("part_1")

	def reset_close2():
		ans = askyesno('Warning', "The partition settings will be deleted after closing the window. \nDo you wish to continue?", parent=self)
		if ans:
			import main
			main.del_partition()
			destroy_w('n')

	def reset_close():
		ans = askyesno('Warning', "The partition settings will be deletedafter closing the window. \nDo you wish to continue?", parent=self)
		if ans:
			undo_part()
			import main
			main.del_partition()
			destroy_w('n')

	def undo_part1(): 
		global All_part, nP, part_name, num, from_n
		setB.config(state=NORMAL)
		if nP>1:
			All_part = All_part[0:int(len(All_part)-2)]
		#	print All_part # USE this to make last check on  partitions 
			texxt.config(state=NORMAL)
			texxt.delete((nP-1.0), END)
			#texxt.insert(END, "\n")
			texxt.config(state=DISABLED)
			nP=nP-1
			name= "part_%s" % nP
			part_name.set(name)			
			try:
				if nP==1: raise
				else:
					num = int(1+All_part[(len(All_part)-1)])
					to_n.set(num)
			except:
				num = 1
				to_n.set(num)
			from_n.set(num)
	def edit_part():
		global setC, editmode
		try:
			setC.config(highlightbackground = "light Grey")
		except:			
			setC = Button(self, text='Set', pady=2, padx=25, command=set_part) #
			setC.grid(row=3,  column=0, sticky=W+E)
			setC.config(highlightbackground = "light Grey", default=ACTIVE)			
		editmode="Yes"
		texxt.config(state=NORMAL)
		setB.config(state=NORMAL)
		picks.entryconfig(0,state=DISABLED)
		showinfo("Manual partitioning", "You can now manually edit the partition settings. RAxML will use the exact text you enter in the field.", parent=self)
		texxt.focus_set()
		def def_part_short(a): set_part()		
		self.bind("<Return>", def_part_short)	

	def export():
		svname = asksaveasfilename(title="Save partition file", parent=self)
		if svname:
			filecontents = texxt.get(1.0, END)
			sv_file = file(svname, 'w')
			sv_file.write(filecontents)

	def import_f():
		(fileinputS) = askopenfilename(title="Import partition file")
		if	fileinputS:
			setB.config(state=DISABLED, default=NORMAL)
			s = file(fileinputS,'U')
			lines = file(fileinputS,'U').read()  # lines = s.readlines()
			texxt.config(state=NORMAL)
			texxt.insert(END, lines)
			texxt.config(state=DISABLED)
			set_part()		

	self = Toplevel()
	self.title( "Set partitions" )
	self.geometry( "570x250" )
	self.config(bg='light Grey')
	self.protocol("WM_DELETE_WINDOW", reset_close2)
	if platform.system() == "Windows" or platform.system() == "Microsoft":
		icon = "%s/icon.ico" % self_path
		self.wm_iconbitmap(icon) 
		self.minsize(460,270)
		self.maxsize(460,270)
	else:
		self.minsize(590,250)
		self.maxsize(590,250)
	#self.withdraw()
	self.grab_set()
	a = Frame(self, relief=RAISED, borderwidth=1)
	labels = Tkinter.Frame(a, relief=FLAT, borderwidth=1)
	labels.grid(row=0,  column=0, sticky=W, columnspan=3)
	labels.config(bg = "light Grey")	
	Label(self, text='   Data type', bg = "light Grey").grid(row=0,  column=0, sticky=W)
	Label(self, text='Partition name  ', bg = "light Grey").grid(row=0,  column=1, sticky=W)
	Label(self, text='from', bg = "light Grey").grid(row=0,  column=2, sticky=W)
	Label(self, text='to', bg = "light Grey").grid(row=0,  column=3, sticky=W)
	Label(labels, text='  Model', bg = "light Grey").grid(row=0,  column=4, sticky=W)
	tool = Tkinter.Frame(a, relief=FLAT, borderwidth=1)
	tool.grid(row=1,  column=0, sticky=W, columnspan=3)
	tool.config(bg = "light Grey")


	### SET CMD
	b = Frame(self, relief=RAISED, borderwidth=1)
	Label(self, text=' ', bg = "light Grey", font=('Times', 30)).grid(row=3,  column=0, sticky=W, columnspan=3)	
	setB = Button(self, text='Add', padx=25, pady=2 , command=def_part) #
	setB.grid(row=3,  column=0, sticky=W)
	setB.config(highlightbackground = "light Grey", default=ACTIVE)
	status= " %s characters, %s" % (maxchar, statusMdtype)
	Label(self, text=status, bg = "light Grey", fg= 'dark blue').grid(row=3,  column=1, sticky=W, columnspan=3)
	mbutton = Menubutton(self, text='Options') #, padx=16)
	mbutton.grid(row=3,  column=4, columnspan=1, sticky=E)
	picks = Menu(mbutton)               
	mbutton.config(menu=picks, bg ="light Grey", relief=RAISED)
	picks.add_command(label='Undo', command=undo_part1)			# EXCLUDE SITES
	picks.add_command(label='Reset partitions', command=undo_part)			# PARTITIONS
	picks.add_command(label='Edit partitions', command=edit_part)			# PARTITIONS
	picks.add_command(label='Import partition file...', command=import_f)			# PARTITIONS	
	picks.add_command(label='Export partition file...', command=export)			# PARTITIONS
	picks.add_command(label='Reset partitions and close...', command=reset_close)			# PARTITIONS

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		texxt = Text(self, padx=35, pady=0, width=40, height=10)
		texxt.grid(row=2,  column=0, sticky=W+E, columnspan=7)
		texxt.config(highlightthickness=0)                 
		sbar = Scrollbar(self, orient=VERTICAL)
		sbar.config(command=texxt.yview)
		texxt.config(yscrollcommand=sbar.set)
		sbar.grid(row=2,  column=0, sticky=N+S+E, columnspan=7)
	else:
		texxt = Text(self, padx=35, pady=0, width=60, height=10)
		texxt.grid(row=2,  column=0, sticky=W+E, columnspan=7)
		texxt.config(highlightthickness=0)                 
		sbar = Scrollbar(self, orient=VERTICAL)
		sbar.config(command=texxt.yview)
		texxt.config(yscrollcommand=sbar.set)
		sbar.grid(row=2,  column=0, sticky=N+S+E, columnspan=7)
	
	def def_part_short(a): def_part()
	self.bind("<Return>", def_part_short)	
	def close_short(a): reset_close2()
	self.bind("<Command-w>", close_short)	
	self.bind("<Control-w>", close_short)	
	self.bind("<Escape>", close_short)	

	
	if platform.system() == "Darwin" or platform.system() == "Windows": texxt.config(relief=GROOVE, bg='#e6e6e6', fg= 'dark blue', font=(11), state=DISABLED)
	else: texxt.config(relief=GROOVE, bg='#e6e6e6', fg= 'dark blue', font=('Monaco', 10), state=DISABLED)
	#texxt.pack(side=LEFT, expand=YES, fill=BOTH)
	if editmode=="Yes":
		texxt.config(state=NORMAL)
		for i in range(0, len(P_list)):
			texxt.insert(END, P_list[i])
 		edit_part()
		nP=len(P_list)
	
	def_part()



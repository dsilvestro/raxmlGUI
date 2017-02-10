#!/usr/bin/env python2.6
# raxmlGUI 1.3.1 build 20141022. A graphical front-end for RAxML.
# Created by Daniele Silvestro and Ingo Michalak on 19/05/2010. 
# For bug reports and support contact raxmlGUI [dot] help [at] gmail [dot] com

import os
import re 

def convert_figtree(tree_file):
	infile=file(tree_file, 'U')
	L=infile.readlines()
	input_file = os.path.basename(tree_file)		 # name input file
	name_file = os.path.splitext(input_file)[0]  # file name without extension
	path_dir = "%s/" % os.path.dirname(tree_file)   # path directory input file
	
	tree=L[0]

	def wtf(obj):
		i1=obj.group(1)
		i2=obj.group(2)
		return i2+i1

	#print tree, "\n"
	convert=re.sub('([:]\d+[.]\d+)[[](\d+)[]]', wtf, tree) 
	out= "%s/%s_figtree.tre" % (path_dir, name_file)
	outfile=file(out, 'wb')
	print out
	outfile.writelines(convert)
	


#for i in re.finditer('([:]\d+[.]\d+)[[](\d+)[]]', tree): print i
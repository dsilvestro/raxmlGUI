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
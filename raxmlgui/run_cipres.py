



if run_CIPRES is True:
	if current_OS == 'Windows': cp_cmd = "copy"
	else: cp_cmd = "cp"
	# create raxml_gui directory
	path_dir_cipres = "%s%s/" % (path_dir,"raxmlgui_cipres")
	os.system("mkdir %s" % path_dir_cipres)
	
	def get_constraint(s): # topology, partitions, outgroup
		type_of_constraint = s.split(" ")[0]
		if type_of_constraint in ["-r","-g","-q","-o"]:
			constr_file= s.split("%s " % (type_of_constraint))[1]
			return [type_of_constraint,constr_file]	
		else:
			return [0,0]
	
	def copy_file(file):
		cmd = "%s %s %s" % (cp_cmd,file,path_dir_cipres)
		os.system(cmd)
	
	def parse_model(mod):                  ### <-----   NEED TO ADD THE OTHER OPTIONS (inv sites, -V, ...)
		mod_list=mod.split(" ")
		ind=mod_list.index("-m")
		subs_model = mod_list[ind+1]
		return [subs_model] ## append other stuff linked to variable 'mod'
	
	def write_to_file(text_str,file_name):
		file="%s%s" % (path_dir_cipres,file_name)
		newfile = open(file, "wb") 
		newfile.writelines(text_str)
		newfile.close()

		
	#__ prepare testInput.properties and copy input files
	input_properties = "infile_=%s\n" % (os.path.basename(seq_file))
	copy_file(seq_file)

	[set_part,part_file] = get_constraint(part_f)
	if set_part != 0: 
		input_properties += "partition_=%s\n" % (os.path.basename(part_file))
		copy_file(part_file)
	
	[set_constr,constr_file] = get_constraint(const_f)
	if set_constr != 0: 
		if set_constr=="-r":
			input_properties += "binary_backbone_=%s\n" % (os.path.basename(constr_file))
		if set_constr=="-g": 
			input_properties += "constraint_=%s\n" % (os.path.basename(constr_file))
		copy_file(constr_file)

	write_to_file(input_properties,"testInput.properties")
	
	#__ prepare testParam.properties
	param_properties =  "toolId=RAXMLHPC2_TGB\n" # can be changed to allow customization
	param_properties += "runtime_=0.50\n"
	param_properties += "outsuffix_=%s\n" % (out_file)
	param_properties += "disable_seqcheck_=1\n"
	param_properties += "dna_gtrcat_=%s\n" % (parse_model(mod)[0])
	
	
	[set_outgroup,outgroup_name] = get_constraint(o)
	if set_outgroup != 0: 
		param_properties += "outgroup_=%s\n" % (outgroup_name)
	
	#__ analysis-specific parameters
	if replicate.get() == 'ML + rapid bootstrap':			
		try int(BSrep.get()): 
			param_properties += "use_bootstopping_=0\n"
			print "HOW TO SET BS NUMBER?"                               ### <-----   CHECK THIS!!!
		except(ValueError): param_properties += "use_bootstopping_=1\n"
			
		param_properties += "bootstrap_seed_val_=%s\nparsimony_seed_val_=%s" % (seed_1,seed_2)
	
	write_to_file(param_properties,"testParam.properties")
	
	print "run some script to start the job!"
	
	


	


	
	
	
		cmd= """cd %s %s        && %s      %s    %s -f a -x %s      %s             %s   -p %s    -N %s       %s  -s %s -n %s %s -O -w %s %s %s %s""" \
% (                  winD, raxml_path,     runWin, K[0], pro,       seed_1, save_brL.get(),mod,  seed_2, BSrep.get(), o, seq_file, out_file, \
part_f, path_dir, const_f, result, winEx)


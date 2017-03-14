#!/usr/bin/env python 
# Created by Daniele Silvestro on 02/03/2012 => dsilvestro@senckenberg.de 
import argparse
import sys

try:
    import python_cipres.commands as CipresCommands
except(ImportError):
    sys.exit("""Module 'requests' not found!""")
p = argparse.ArgumentParser()  # description='<input file>')
p.add_argument('-v', action='version', version='%(prog)s')
p.add_argument('-d', type=str, help='path_dir_cipres', default="")
p.add_argument('-e', type=str, help='type_of_run', default="run")
p.add_argument('-wd', type=str, help='working directory', default="")  # results will be downloaded there
p.add_argument('-n', type=str, help='job name', default="")
p.add_argument('-m', type=str, help='email', default="0")
args = p.parse_args()

try:
    CipresCommands.tooltest([0, args.d, args.e, args.wd, args.n, args.m])
except:
    "Something went wrong!"

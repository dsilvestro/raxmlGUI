#!/usr/bin/env python2.6
# raxmlGUI 1.3.1 build 20141022. A graphical front-end for RAxML.
# Created by Daniele Silvestro and Ingo Michalak on 19/05/2010. 
# For bug reports and support contact raxmlGUI [dot] help [at] gmail [dot] com


import sys
import os 
import os.path
import raxmlGUI

self_path = os.getcwd()
self_path = "%s/raxmlgui" % self_path
self_path_mod = """ "%s" """ % self_path
raxml_path = """ "%s/raxml" """% self_path
from raxmlgui import main
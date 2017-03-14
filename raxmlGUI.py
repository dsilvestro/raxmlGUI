#!/usr/bin/env python 
# raxmlGUI 1.3 build 20120118. A graphical front-end for RAxML.
# Project started in March 2010
# Created by Daniele Silvestro and Ingo Michalak on 19/05/2010.

import os
import os.path

self_path = os.getcwd()
self_path = "%s/raxmlgui" % self_path
self_path_mod = """ "%s" """ % self_path
raxml_path = """ "%s/raxml" """ % self_path
from raxmlgui import main
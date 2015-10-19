raxmlGUI -- A graphical front-end for RAxML

Silvestro, D. & Michalak, I. (2012) raxmlGUI: A graphical front-end for RAxML. 

General Info
----------------------------------------
raxmlGUI version 1.3 has been tested under Mac (Intel 64bit; OS 10.6, 10.7)
Windows (XP, 7), and Linux (Ubuntu) using Python 2.5-2.7.
The package includes executable files of RAxML 7.4.2 (Stamatakis, 2006) 
compiled for the different operating systems.

raxmlGUI does not support Python 3.


Release Notes version 1.31
----------------------------------------
* small UI fixes for Mac OSX 10.9 (Mavericks)

Release Notes version 1.3
----------------------------------------
* A bug introduced in the previous version that prevented the concatenation of
  alignments  was fixed
* Updated RAxML executable with support for FASTA files

Contacts
----------------------------------------
Please report suggestions and bugs to:
	raxmlgui.help@gmail.com	

To receive updates notifications join raxmlGUI mailing list at:
	https://lists.sourceforge.net/lists/listinfo/raxmlgui-news


Known issues
----------------------------------------
On Mac OS 10.6 unexpected crashes have been reported.
Work-around: a downgrade to Python 2.6 seems to fix the problem


Run raxmlGUI
----------------------------------------
To run raxmlGUI on a Mac simply copy "raxmlGUI.app" to your Applications
folder and double click on "raxmlGUI.app". Note that, since version 0.93,
raxmlGUI is launched using AppleScript thus adapting to the Python version
you have installed on your machine (2.5-2.7). 

To run the Multi-platform release of raxmlGUI you can launch the file 
"raxmlGUI.py" with a double click (Windows), or browse through the Terminal 
to the program directory using

"cd ~/.../raxmlGUI1.3" 

and type

"./raxmlGUI.py" or "python raxmlGUI.py" (UNIX)

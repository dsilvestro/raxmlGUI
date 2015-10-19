raxmlGUI -- A graphical front-end for RAxML
                   version 1.5b1, June 2015
----------------------------------------

Silvestro, D. & Michalak, I. (2012) raxmlGUI: A graphical front-end for RAxML. 
Organisms Diversity & Evolution 12, 335-337, DOI: 10.1007/s13127-011-0056-0

General Info
----------------------------------------
raxmlGUI version 1.5b1 has been tested Windows 7, and Linux (Ubuntu 14.04) 
using Python 2.7.
The package includes executable files of RAxML 8.1.2 (Stamatakis, 2014) 
compiled for different operating systems (Windows, Ubuntu, OSX).
It is recommended on UNIX systems to compile appropriate RAxML executables
(AVX[2], PTHREADS).

raxmlGUI does not support Python 3.

You can download an updated Manual and example files here:
https://sourceforge.net/projects/raxmlgui/files/.


Release Notes version 1.5b1
----------------------------------------
This is a beta version! 

This version of raxmlGUI you can run your analyses (currently with limited
functions) using the CIPRES Science Gateway (Miller et al. 2011) via the
REST API (Miller et al. 2015). You will need to install the necessary
python toolkit, kindly provided by Terri Schwartz from the SDSC and
included in the package.

Further details are provided in the updated manual. For additional info,
suggestions, bug reports please contact us at raxmlgui.help@gmail.com.
You can download previous stable versions orf raxmlGUI at
http://sourceforge.net/projects/raxmlgui/files/.


Contacts
----------------------------------------
Please report suggestions and bugs to:
	raxmlgui.help@gmail.com	

To receive updates notifications join raxmlGUI mailing list at:
	https://lists.sourceforge.net/lists/listinfo/raxmlgui-news


Known issues
----------------------------------------
On Mac OS 10.6 unexpected crashes have been reported.
Work-around: a downgrade to Python 2.6 seems to fix the problem.


Run raxmlGUI
----------------------------------------

To run this Multi-platform release of raxmlGUI you can launch the file 
"raxmlGUI.py" with a double click (Windows), or browse through the Terminal 
to the program directory using

"cd ~/.../raxmlGUI1.5b1" 

and type

"raxmlGUI.py", "./raxmlGUI.py" or "python raxmlGUI.py" (depending on the OS)

More details are provided in the Manual. 

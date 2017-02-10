1. From this directory, run "python setup.py install"
	You may need to use virtualenv or have sudo/root access or use --prefix or --user. 

2. Follow the registration instructions in the "Getting Started Guide" 
(https://www.phylo.org/restusers/docs/guide.html#Register) to create an account for 
yourself, login and register/create an application.   

3. In your home directory create a file called "pycipres.conf" with the following settings:

	URL=https://www.phylo.org/cipresrest/v1				
	APPNAME=the_application_you_just_registered
	APPID=its_app_id
	USERNAME=the_username_you_just_registerd
	PASSWORD=the_password


python_cipres is 

	a) an example showing how to use the CIPRES REST API from python:
		Look at bin/tooltest.py and the code it wraps in python_cipres/commands.py and
		python_cipres/client.py.

	b) a python library that you can use to access the REST API:
		import python_cipres.client as CipresClient

	c) There are a couple of scripts in python_cipres/python_cipres/bin: tooltest.py
	and cipresjob.py that can be run from the command line to submit jobs, list jobs, download
	results, etc.  For more info about running these scripts, see
	examples/Readme.txt

python_cipres was written for python 2.7 and tested on linux, mac OS and windows.

If you base an application on this code, keep in mind that the users of your application
should use the APPNAME and APPID that you register, but must use their own USERNAME
and PASSWORD.






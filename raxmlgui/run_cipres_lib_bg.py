#!/usr/bin/env python 
# Created by Daniele Silvestro on 02/03/2012 => dsilvestro@senckenberg.de 
import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET

import requests

import python_cipres.client as CipresClient
import python_cipres.pyjavaproperties as Props


def tooltest(argv):
    if not argv or len(argv) < 3:
        print tooltest.__doc__
        return 1

    template = argv[1]
    action = argv[2]
    job_name = argv[4].replace("_", " ")
    metadata = {'clientJobName': job_name, 'statusEmail': 'true'}

    if not os.path.isdir(template):
        print "%s is not a valid TEMPLATE_DIRECTORY" % (template)
        print tooltest.__doc__
        return 1

    if action != "validate" and action != "run":
        print "second argument must be either validate or run"
        print tooltest.__doc__
        return 1
    resultsdir = None
    if len(argv) > 3:
        resultsdir = argv[3]

    properties = CipresClient.Application().getProperties()
    client = CipresClient.Client(properties.APPNAME, properties.APPID, properties.USERNAME, properties.PASSWORD,
                                 properties.URL)
    try:
        if action == "validate":
            job = client.validateJobTemplate(template)
            job.show()
        else:
            job = client.submitJobTemplate(template, metadata)
            job.show(messages="true")
            print "Job's running ..."
            # job.waitForCompletion()
            # if not resultsdir:
        #	resultsdir = job.jobHandle
        # if not os.path.exists(resultsdir):
        #	os.mkdir(resultsdir)
    # print "Downloading results to %s" % (os.path.abspath(resultsdir))
    # job.downloadResults(directory=resultsdir)
    except CipresClient.ValidationError as ve:
        print ve.asString()
        return 2
    except CipresClient.CipresError as ce:
        print "CIPRES ERROR: %s" % (ce)
        return 2
    except requests.exceptions.RequestException as e:
        print "CONNECTION ERROR: %s" % (e)
        return 2
    return 0


p = argparse.ArgumentParser()  # description='<input file>')
p.add_argument('-v', action='version', version='%(prog)s')
p.add_argument('-d', type=str, help='path_dir_cipres', default="")
p.add_argument('-e', type=str, help='type_of_run', default="run")
p.add_argument('-wd', type=str, help='working directory', default="")  # results will be downloaded there
p.add_argument('-n', type=str, help='job name', default="")
args = p.parse_args()

try:
    tooltest([0, args.d, args.e, args.wd, args.n])
except:
    "Something went wrong!"

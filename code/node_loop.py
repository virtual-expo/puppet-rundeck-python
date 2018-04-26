#!/usr/bin/env python3
#coding: utf8
#  vim: set sw=4

#, sys, time

import os
from stat import *
from datetime import datetime, timedelta
import glob
from code.helper import *
from code.generate_yaml import *
from code.add_nodes import *
import tempfile

def generate_node(filehandle,outputfile,max_age,path_to_node):
    if (datetime.now() - datetime.fromtimestamp(os.path.getmtime(path_to_node))) > timedelta(days = max_age):
        log("file %s is too old" % path_to_node)
    else:
        node_dot_yaml = os.path.basename(path_to_node) 
        generate_yaml(path_to_node,filehandle,node_dot_yaml)


def node_loop(yaml_node_dir, outfile, max_age):

    log("Puppet yaml/node directory set to: %s" % yaml_node_dir)

    listing = glob.glob(yaml_node_dir + '/*.yaml')

    filehandle = tempfile.NamedTemporaryFile(mode='w', prefix='puppet-to-rundeck', dir=os.path.dirname(outfile))
    os.chmod(filehandle.name, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH)

    logv('adding special nodes')
    add_nodes(filehandle)
    logv('special nodes added')
    
    for path_to_node in listing:
        generate_node(filehandle, outfile, max_age, path_to_node)

    logv('end of the loop')

    # remove the real outfile and create a new hardlink
    os.remove(outfile)
    os.link(filehandle.name, outfile)

    # python automagically removes the tempfile
    filehandle.close

#!/usr/bin/env python3
#coding: utf8
#  vim: set sw=4

#, sys, time

import os
from datetime import datetime, timedelta
import glob
from code.helper import *
from code.generate_yaml import *

def generate_node(outputdir,max_age,path_to_node):
    if (datetime.now() - datetime.fromtimestamp(os.path.getmtime(path_to_node))) > timedelta(days = max_age):
        log("file %s is too old" % path_to_node)
    else:
        node_dot_yaml = os.path.basename(path_to_node) 
        generate_yaml(path_to_node,outputdir,node_dot_yaml)


def node_loop(yaml_node_dir,outputdir,max_age,rq_path):

    log("Puppet yaml/node directory set to: %s" % yaml_node_dir)

    if rq_path == '/':
        listing = glob.glob(yaml_node_dir + '/*.yaml')
        for path_to_node in listing:
            generate_node(outputdir,max_age,path_to_node)

        logv('end of the loop')
    else:
        path_to_node = yaml_node_dir + rq_path
        generate_node(outputdir,max_age,path_to_node)

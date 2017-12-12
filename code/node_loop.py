#!/usr/bin/env python3
#coding: utf8
#  vim: set sw=4

import yaml
import argparse
import os, sys, time
from itertools import islice
from datetime import datetime, timedelta
import glob
from code.generate_yaml import *


def node_loop(yaml_node_dir,outputdir):

    print ("Puppet yaml/node directory set to: %s" % yaml_node_dir)

    listing = glob.glob(yaml_node_dir + '*.yaml')

    for path_to_node in listing:
        if (datetime.now() - datetime.fromtimestamp(os.path.getmtime(path_to_node))) > timedelta(days = 1):
            print("file %s is too old" % path_to_node)
            continue
        else:
            node_dot_yaml = os.path.basename(path_to_node) 

            generate_yaml(path_to_node,outputdir,node_dot_yaml)

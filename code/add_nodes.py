#!/usr/bin/env python3
#coding: utf8
#  vim: set sw=4

import yaml
import argparse
import os, sys, time
from itertools import islice
from datetime import datetime, timedelta
import glob
from code.helper import *


def add_nodes(filehandle):
    conf_file = 'conf/other_nodes.yaml'

    if not os.path.isfile(conf_file):
        log("no addtional nodes declared")
    else:
        log("adding nodes from file: %s" % conf_file)
        f = open(conf_file, 'r')
        d = yaml.load(f)

        yaml.dump(d, filehandle, default_flow_style=False)

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
    
    
    d = {'velo4nas11':
            {'hostname': 'velo4nas11',
             'tags': ['nas'],
             'datacenter': 'lo',
             'nodetype': 'nas',
            }
         
         'velo4nas12':
            {'hostname': 'velo4nas12',
             'tags': ['nas'],
             'datacenter': 'lo',
             'nodetype': 'nas',
            }
        }

    yaml.dump(d, filehandle, default_flow_style=False)

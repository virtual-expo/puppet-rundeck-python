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



def cut_line_1(fin,tmp_file):
    with open(fin, 'r') as f0:
        data = f0.read().splitlines(True)
    with open(tmp_file, 'w') as fout:
        fout.writelines(data[1:])

def generate_yaml(path, filehandle, node):
    tmp_file = '/tmp/tmpfile.yaml'
    tags_list = ['datacenter', 'node_environment', 'node_type', 'node_envid', 'lsbdistcodename']
    attributes_list = ['node_envid', 'datacenter', 'node_instanceid', 'node_environment', 'lsb_distcodename', 'node_type']

    logv("working on file: %s" % path)

    if not os.path.isfile(path):
        print('file does not exist: %s' % path)
        sys.exit(1)
    else:
        cut_line_1(path,tmp_file)
        f = open(tmp_file, 'r')
        yaml_data = yaml.load(f)
        tags = []

        # check tags exist
        for tag_item in tags_list:
            if not tag_item in yaml_data['parameters']:
                print('WARN: tag %s does not exist for file: %s' % (tag_item, path))
            else:
                tags.append(yaml_data['parameters'][tag_item])

        attributes = { }

        for attribute in attributes_list:
            if not attribute in yaml_data['parameters']:
                print('WARN: attribute %s does not exist for file: %s' % (attribute, path))
                attributes[attribute] = "__unknown__"
            else:
                attributes[attribute] = yaml_data['parameters'][attribute]

        try:

            d = {yaml_data['parameters']['hostname']:
                   {'hostname':yaml_data['name'],
                    'osFamily':yaml_data['parameters']['osfamily'],
                    'osVersion':yaml_data['parameters']['os']['release']['full'],
                    'osName':yaml_data['parameters']['os']['lsb']['distdescription'],
                    'osArch':yaml_data['parameters']['architecture'],
                    'tags': tags,
                    'envid': attributes['node_envid'],
                    'datacenter': attributes['datacenter'],
                    'instanceid': attributes['node_instanceid'],
                    'environment': attributes['node_environment'],
                    'lsbdistcodename': attributes['lsb_distcodename'],
                    'nodetype': attributes['node_type'],
                   }
                }

                yaml.dump(d, filehandle, default_flow_style=False)
        except TypeError:
            print('ERROR: TypeError caught, skipping node %s.' % node)

        f.close()


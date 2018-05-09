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

def lookup_yaml(yaml_data,keys,node):
    value = yaml_data
    for key in keys.split('.'):
        logv("looking for key %s" % key)
        if isinstance(value, dict):
            if not key in value:
                log('key %s does not exist for node: %s' % (key, node))
                value = "__unknown__"
            else:
                value = value[key]
        else:
            log('key %s cannot be read for node %s' % (key,node))
            value = "__unknown__"
            break
    return value

def generate_yaml(path, filehandle, node):
    with open('conf/conf.yaml', 'r') as ymlconf:
        cfg = yaml.load(ymlconf)

    tmp_file = cfg['tmp_file']
    tags_list = cfg['tags_list']

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
                print('WARN: tag %s does not exist for node: %s' % (tag_item, node))
            else:
                tags.append(yaml_data['parameters'][tag_item])

        try:
            sub_dict = {}
            for key in cfg['yamlstruct']['keys']:
                sub_dict[key] = lookup_yaml(yaml_data,cfg['yamlstruct']['keys'][key],node)
                #print(sub_dict)

            d = {lookup_yaml(yaml_data,cfg['yamlstruct']['node_name'],node):sub_dict}
            
            yaml.dump(d, filehandle, default_flow_style=False)
        except TypeError:
            log('ERROR: TypeError caught, skipping node %s.' % node)

        f.close()


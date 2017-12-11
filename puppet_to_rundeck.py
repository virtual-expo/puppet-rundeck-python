#!/usr/bin/env python3
#coding: utf8
#  vim: set sw=4

import yaml
import argparse
import os, sys, time
from itertools import islice
from datetime import datetime, timedelta
import glob



def cut_line_1(fin,tmp_file):
    with open(fin, 'r') as f0:
        data = f0.read().splitlines(True)
    with open(tmp_file, 'w') as fout:
        fout.writelines(data[1:])

def puppet_to_rundeck(path,outputdir,node):
    tmp_file = outputdir + '/tmp/tmpfile.yaml'

    print("working on file: %s" % path)

    if not os.path.isfile(path):
        print('file does not exist: %s' % path)
        sys.exit(1)
    else:
        cut_line_1(path,tmp_file)
        f = open(tmp_file, 'r')
        yaml_data = yaml.load(f)

        tags = yaml_data['parameters']['datacenter'] + ',' + yaml_data['parameters']['node_environment'] + ',' + yaml_data['parameters']['node_type'] + ',' + yaml_data['parameters']['os']['lsb']['distcodename']
        d = {yaml_data['parameters']['hostname']:{'hostname':yaml_data['name'], 'osFamily':yaml_data['parameters']['osfamily'], 'osVersion':yaml_data['parameters']['os']['release']['full'], 'osName':yaml_data['parameters']['os']['lsb']['distdescription'], 'osArch':yaml_data['parameters']['architecture'], 'tags':tags}}
        f.close()

        with open(outputdir + '/node/' + node + '.yaml', 'w') as result_file:
            yaml.dump(d, result_file, default_flow_style=False)


def main():
    parser = argparse.ArgumentParser(description='Loads yaml')
    parser.add_argument('-y', '--yamldir', required=True, default='./yaml', help='path to the yaml directory', type=str)
    parser.add_argument('-o', '--outputdir', required=True, default='./outdir', help='path to the outgoing directory', type=str)

    args = parser.parse_args()
    yaml_node_dir = args.yamldir + '/node/'
    print ("yaml_node_dir: %s" % yaml_node_dir)

    listing = glob.glob(yaml_node_dir + '*.yaml')
    for path_to_node in listing:
        node = os.path.basename(path_to_node) 
        if (datetime.now() - datetime.fromtimestamp(os.path.getmtime(path_to_node))) > timedelta(days = 1):
            print("file %s is too old" % path_to_node)
            continue
        else:
            puppet_to_rundeck(path_to_node,args.outputdir,node)

if __name__ == "__main__":
    main()

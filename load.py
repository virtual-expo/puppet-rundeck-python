#!/usr/bin/env python3
#coding: utf8
#  vim: set sw=4

import yaml
import argparse
import os, sys
from itertools import islice


def cut_line_1(fin,tmp_file):
    with open(fin, 'r') as f0:
        data = f0.read().splitlines(True)
    with open(tmp_file, 'w') as fout:
        fout.writelines(data[1:])

def puppet_to_rundeck(yaml_node_dir,outputdir,node):
    tmp_file = outputdir + '/tmp/tmpfile.yaml'
    path = yaml_node_dir + node
    print("file: %s" % path)

    if not os.path.isfile(path):
        print('file does not exist: %s' % path)
        sys.exit(1)
    else:
        cut_line_1(path,tmp_file)
        f = open(tmp_file, 'r')
        yaml_data = yaml.load(f)

        tags = yaml_data['parameters']['datacenter'] + ',' + yaml_data['parameters']['node_environment'] + ',' + yaml_data['parameters']['node_type']
        d = {yaml_data['parameters']['hostname']:{'hostname':yaml_data['name'], 'osFamily':yaml_data['parameters']['osfamily'], 'osVersion':yaml_data['parameters']['os']['release']['full'], 'osName':yaml_data['parameters']['os']['lsb']['distdescription'], 'tags':tags}}
        f.close()

        with open(outputdir + '/node/' + node + '.yaml', 'w') as result_file:
            yaml.dump(d, result_file, default_flow_style=False)


def main():
    parser = argparse.ArgumentParser(description='Loads yaml')
    parser.add_argument('-y', '--yamldir', required=True, default='./yaml', help='path to the yaml directory', type=str)
    parser.add_argument('-o', '--outputdir', required=True, default='./outdir', help='path to the outgoing directory', type=str)

    args = parser.parse_args()
    yaml_node_dir = args.yamldir + '/node/'

    for node in os.listdir(yaml_node_dir):
        puppet_to_rundeck(yaml_node_dir,args.outputdir,node)

if __name__ == "__main__":
    main()

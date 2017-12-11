#!/usr/bin/env python3
#coding: utf8
#  vim: set sw=4

import yaml
import argparse
import os, sys
from itertools import islice


# concatenate all its arguments, adding '/' between elements
def makepath(*arg):
    result = ""
    for i in arg:
        if result == "":
            result += i
        else:
            result += ( '/' + str(i) )
            return result

def cut_line_1(fin,tmp_file):
    with open(fin, 'r') as f0:
        data = f0.read().splitlines(True)
    with open(tmp_file, 'w') as fout:
        fout.writelines(data[1:])


def main():
    parser = argparse.ArgumentParser(description='Loads yaml')
    parser.add_argument('-y', '--yamldir', required=True, default='./yaml', help='path to the yaml directory', type=str)
    parser.add_argument('-t', '--tmpdir', required=True, default='./tmpdir', help='path to the temporary directory', type=str)

    args = parser.parse_args()

    tmp_file = args.tmpdir + '/file.yaml'
    path = args.yamldir + '/node/' + 'velo1dblx01.virtual-expo.com.yaml'
    print("file: %s" % path)

    if not os.path.isfile(path):
        print('file does not exist: %s' % path)
        sys.exit(1)
    else:
        cut_line_1(path,tmp_file)
        with open(tmp_file, 'r') as f1:
            try:
                print(yaml.load(f1))
            except:
                raise

if __name__ == "__main__":
    main()

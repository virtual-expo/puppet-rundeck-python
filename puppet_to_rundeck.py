#!/usr/bin/env python3
#coding: utf8
#  vim: set sw=4

import argparse, os, sys
from code.helper import *
from code.node_loop import node_loop


def main():
    parser = argparse.ArgumentParser(description='Reads in puppet yaml dir to make a list of nodes for rundeck')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='verbose logging')
    parser.add_argument('-o', '--outfile', type=str, help='output file', required=True)
    parser.add_argument('-i', '--inputdir', default='/var/lib/puppet/yaml/node', type=str, help='input directory')
    parser.add_argument('-m', '--maxage', type=int, default=7, help='max age of input node files (days)')

    args = parser.parse_args()
    logv_set(args.verbose)
    
    if not os.path.isdir(args.inputdir):
        print('ERROR: directory does not exist or is not readable: %s' % args.inputdir)
        sys.exit(1)
    else:
        node_loop(args.inputdir, args.outfile, args.maxage)

if __name__ == "__main__":
    main()

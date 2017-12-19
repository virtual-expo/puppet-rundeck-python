#!/usr/bin/env python3
#coding: utf8
#  vim: set sw=4

import argparse
from code.server import *
from code.helper import *


def main():
    parser = argparse.ArgumentParser(description='Reads in puppet yaml dir to make a list of nodes for rundeck')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='verbose logging')

    args = parser.parse_args()
    logv_set(args.verbose)
    
    runServer()

if __name__ == "__main__":
    main()

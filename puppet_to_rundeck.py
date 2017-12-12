#!/usr/bin/env python3
#coding: utf8
#  vim: set sw=4

import argparse
from code.server import *
from code.helper import *


def main():
    parser = argparse.ArgumentParser(description='Reads in puppet yaml dir to make a list of nodes for rundeck')
    parser.add_argument('-p', '--port', required=False, default=8080, help='port to listen on', type=int)
    parser.add_argument('-b', '--bind', required=False, default='127.0.0.1', help='address to bond to', type=str)
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='verbose logging')

    args = parser.parse_args()
    logv_set(args.verbose)
    
    runServer(args.bind,args.port)

if __name__ == "__main__":
    main()

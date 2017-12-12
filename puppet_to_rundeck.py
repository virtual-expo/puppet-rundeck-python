#!/usr/bin/env python3
#coding: utf8
#  vim: set sw=4

import yaml
import argparse
import os, sys, time
from itertools import islice
from datetime import datetime, timedelta
import glob
from code.server import *


def main():
    parser = argparse.ArgumentParser(description='Reads in puppet yaml dir to make a list of nodes for rundeck')
    parser.add_argument('-p', '--port', required=False, default=8080, help='port to listen on', type=int)
    parser.add_argument('-b', '--bind', required=False, default='127.0.0.1', help='address to bond to', type=str)

    args = parser.parse_args()
    
    runServer(args.bind,args.port)
    #node_loop(args.yamlnodedir,args.outputdir)


if __name__ == "__main__":
    main()

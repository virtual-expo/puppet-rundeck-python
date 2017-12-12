#!/usr/bin/env python3

import time

def logv_set(flag):
    global g_verbose
    g_verbose = flag

def logv(str):
    global g_verbose
    if g_verbose:
        print('[' + time.strftime("%c") + '] ' + str)

def log(str):
    print('[' + time.strftime("%c") + '] ' + str)

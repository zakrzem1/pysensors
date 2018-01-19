from __future__ import print_function
import sys
import datetime

def warning(*objs):
  print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\tWARNING: ", objs, file=sys.stderr)

def info(*objs):
  print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\tINFO: ", objs, file=sys.stderr)

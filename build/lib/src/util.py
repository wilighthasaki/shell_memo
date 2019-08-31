#!/usr/bin/python
import os
import subprocess


def get_size():
    height, width = map(int, subprocess.getoutput("stty size").strip().split())
    return height, width

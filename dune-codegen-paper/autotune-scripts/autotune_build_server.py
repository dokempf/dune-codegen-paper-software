#!/usr/bin/env python

"""
This is a small server-like application that can run commands that were written
to a file. This is necessary to separate the code generation process from the
autotune run environment, using the file system for synchronization.
"""

import filelock
import os
import subprocess
import sys
import time

filename = "tasks.txt"
open(filename, "w").close()
lock = "{}.lock".format(filename)
arg_prefix = sys.argv[1:]

keep_running = True
while keep_running:
    with filelock.FileLock(lock):
        with open(filename, "r") as f:
            lines = f.readlines()

    command = None
    if lines:
        command = lines[0].strip("\n")

    if command == "exit":
        keep_running = False
        command = None

    if command is not None:
        subprocess.call(arg_prefix + command.split())
    
        with filelock.FileLock(lock):
            with open(filename, "r") as f:
                lines = f.readlines()

            with open(filename, "w") as f:
                for line in lines[1:]:
                    f.write(line)

    time.sleep(0.1)

os.remove(filename)
os.remove(lock)

#!/usr/bin/env python

import filelock
import sys
import time

filename = "/home/dkempf/dune-codegen-paper-software/tasks.txt"
lock = "{}.lock".format(filename)
command = " ".join(sys.argv[1:])

# Submit the command into the queue
with filelock.FileLock(lock):
    with open(filename, "a") as f:
        f.write("{}\n".format(command))

# Poll the queue for our command still being in
while True:
    found = False
    for line in open(filename, "r"):
        if command in line:
            found = True

    if not found:
        sys.exit(0)

    time.sleep(0.1)

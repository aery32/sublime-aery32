"""
https://gist.github.com/4100575
Usage: python fixhudson.py [path_to_avrtoolchain]
"""

import os
import subprocess

def which(executable):
    """ Mimics Linux / Unix Command: which """
    from os.path import join, isfile

    for path in os.environ['PATH'].split(os.pathsep):
        target = join(path, executable)
        if isfile(target) or isfile(target + '.exe'):
            return path
    return None

def strip_avrlibs(path_to_avrtoolchain):
    path = os.path.join(path_to_avrtoolchain, "avr/lib")
    if not os.path.isdir(path):
        return False

    for root, dirs, files in os.walk(path):
        names = [name for name in files if name.endswith((".o", ".a"))]
        if names:
            cmd = "avr-strip -g " + " ".join(names)
            subprocess.Popen(cmd, cwd=root)

def strip_avr32libs(path_to_avrtoolchain):
    path = os.path.join(path_to_avrtoolchain, "avr32/lib")
    if not os.path.isdir(path):
        return False

    for root, dirs, files in os.walk(path):
        names = [name for name in files if name.endswith((".o", ".a"))]
        if names:
            cmd = "avr32-strip -g " + " ".join(names)
            subprocess.Popen(cmd, cwd=root)

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        path_to_avrgcc = which("avr-gcc")
        if not path_to_avrgcc:
            path_to_avrgcc = which("avr32-gcc")
        if not path_to_avrgcc:
            sys.exit(1)
        path_to_avrtoolchain = os.path.join(path_to_avrgcc, "..")
    else:
        path_to_avrtoolchain = sys.argv[1]
        os.environ["PATH"] += os.pathsep + os.path.join(path_to_avrtoolchain, "bin")

    strip_avrlibs(path_to_avrtoolchain)
    strip_avr32libs(path_to_avrtoolchain)
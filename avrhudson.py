import os
import subprocess

def strip_avrlibs(path_to_avrtoolchain):
    path = os.path.join(path_to_avrtoolchain, "avr/lib")
    path = os.path.normpath(path)
    if not os.path.isdir(path):
        return False

    for root, dirs, files in os.walk(path):
        strip_these = [f for f in files if f.endswith(".o") or f.endswith(".a")]
        if strip_these:
                subprocess.Popen("avr-strip -g " + " ".join(strip_these), cwd=root)

def strip_avr32libs(path_to_avrtoolchain):
    path = os.path.join(path_to_avrtoolchain, "avr32/lib")
    path = os.path.normpath(path)
    if not os.path.isdir(path):
        return False

    for root, dirs, files in os.walk(path):
        strip_these = [f for f in files if f.endswith(".o") or f.endswith(".a")]
        if strip_these:
            subprocess.Popen("avr32-strip -g " + " ".join(strip_these), cwd=root)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s path_to_avrtoolchain" % sys.argv[0])
        sys.exit(1)

    strip_avrlibs(sys.argv[1])
    strip_avr32libs(sys.argv[1])

#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = [
        os.path.join(pkg_dir, "share/scripts/yaml2uvmf.py")
    ]

    cmd.extend(sys.argv[1:])

    res = subprocess.run(cmd)

    if res.returncode != 0:
        raise Exception("run failed")
    pass

if __name__ == "__main__":
    main()

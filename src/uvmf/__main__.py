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

    # Add in IVPM-provided paths (if available)
    try:
        import ivpm
        from ivpm.utils import find_project_root, load_project_package_info

        paths = []
        project_root = find_project_root(os.getcwd())
        if project_root is not None:
            info = load_project_package_info(project_root)
            for ii,i in enumerate(info):
                key = "project" if ii == 0 else "export"
                if key in i.paths.keys():
                    exp = i.paths[key]
                    if "uvmf" in exp.keys():
                        for path in exp["uvmf"]:
                            if os.path.isfile(path):
                                paths.append(path)
                            elif os.path.isdir(path):
                                for f in os.listdir(path):
                                    ext = os.path.splitext(f)[1]
                                    if ext in [".yaml", ".yml", ".uvmf"]:
                                        paths.append(os.path.join(path, f))
        
        rgy = ivpm.PkgInfoRgy.inst()
        for path in rgy.getPaths("uvmf"):
            if os.path.isfile(path):
                paths.append(path)
            elif os.path.isdir(path):
                for f in os.listdir(path):
                    ext = os.path.splitext(f)[1]
                    if ext in [".yaml", ".yml", ".uvmf"]:
                        paths.append(os.path.join(path, f))

        print("Note: Added IVPM-specified YAML file: %s" % str(paths))
        cmd.extend(paths)
    except Exception as e:
        print("Note: IVPM not available: %s" % str(e))

    res = subprocess.run(cmd)

    if res.returncode != 0:
        raise Exception("run failed")
    pass

if __name__ == "__main__":
    main()

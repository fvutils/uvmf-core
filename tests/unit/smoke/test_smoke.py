import os
import shutil
import subprocess
import sys
import pytest_fv
from pytest_fv import FuseSoc, HdlToolSimRgy

def test_smoke():
    testdir = os.path.dirname(os.path.abspath(__file__))
    rundir = os.path.join(testdir, "rundir")
    uvmf_core_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../.."))
    
    # if os.path.isdir(rundir):
    #     shutil.rmtree(rundir)

    # os.makedirs(os.path.join(rundir, "verif"))



    cmd = [
        sys.executable,
        os.path.join(uvmf_core_dir, "scripts/yaml2uvmf.py"),
        "-m",
        os.path.join(rundir, "verif"),
        os.path.join(testdir, "mem_if_cfg.yaml"),
        os.path.join(testdir, "pkt_if_cfg.yaml"),
        os.path.join(testdir, "block_a_env_cfg.yaml"),
        os.path.join(testdir, "block_a_bench_cfg.yaml"),
        os.path.join(testdir, "predictor_components.yaml")
    ]

    # res = subprocess.run(
    #     cmd,
    #     cwd=rundir,
    #     stdout=sys.stdout,
    #     stderr=sys.stdout
    # )

    fs = FuseSoc()
    fs.add_library(
        os.path.join(uvmf_core_dir, "uvmf_base_pkg"),
        ignore={"tests","packages"}
    )
    fs.add_library(
        os.path.join(rundir, "verif"),
        ignore={"tests","packages"}
    )

    try:
        files = fs.getFiles(
            "uvmf:project_benches:block_a",
            flags={"sv-uvm": True})
        print("files: %s" % str(files), flush=True)
        sim = HdlToolSimRgy.get("xsim")
        sim.addFiles(files, {"sv-uvm": True})
        sim.build()
    except Exception as e:
        print("Exception: %s" % str(e), flush=True)

#    assert res.returncode == 1
    assert False

    pass
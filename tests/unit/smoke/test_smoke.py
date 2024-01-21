import os
import shutil
import subprocess
import sys
import pytest_fv
from pytest_fv import FuseSoc, HdlSim

def test_smoke():
    testdir = os.path.dirname(os.path.abspath(__file__))
    rundir = os.path.join(testdir, "rundir")
    uvmf_core_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../.."))
    
    if os.path.isdir(rundir):
        shutil.rmtree(rundir)

    os.makedirs(os.path.join(rundir, "verif"))

    cmd = [
        sys.executable,
        os.path.join(uvmf_core_dir, "scripts/yaml2uvmf.py"),
        "-m",
        os.path.join(rundir, "verif"),
        os.path.join(testdir, "test.uvmf")
    ]

    res = subprocess.run(
        cmd,
        cwd=rundir,
        stdout=sys.stdout,
        stderr=sys.stdout
    )

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
            "uvmf:project_benches:my_bench",
            flags={"sv-uvm": True})
        print("files: %s" % str(files), flush=True)
        sim = HdlSim.create("xsm")
        build_args = sim.mkBuildArgs(os.getcwd())
        build_args.addFiles(files, {"sv-uvm": True})
        build_args.top.add("hdl_top")
        build_args.top.add("hvl_top")
        sim.build(build_args)
    except Exception as e:
        print("Exception: %s" % str(e), flush=True)

    run_args = sim.mkRunArgs(
        build_args.builddir,
        build_args.builddir)
    run_args.plusargs.append("UVM_TESTNAME=test_top")
    
    sim.run(run_args)

    assert res.returncode == 0

    pass


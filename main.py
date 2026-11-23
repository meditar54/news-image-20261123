#!/usr/bin/env python3
"""News-image entry (Python 3.13, standard library only): the image is the
entry.png beside this file, and the program copies it to the output
directory. Deterministic: the same bytes every run, no network.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(
    os.path.join(HERE, "entry.png"),
    os.path.join(OUT, "entry.png"),
)

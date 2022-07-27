#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing
import subprocess
import os.path
import sys

NUMBER_OF_TASKS = 2


def work(fpath: str):
    # fpath = './FromHosttoTohost,srcIP,dstIP.log'
    srcIP = os.path.basename(fpath).split(",")[1]
    dstIP = os.path.basename(fpath).split(",")[2].split(".", 1)[0]
    print(
        "Start transmission spoof "
        + os.path.basename(fpath).split(",")[0].split("to")[0]
        + "("
        + srcIP
        + ") to "
        + os.path.basename(fpath).split(",")[0].split("to")[1]
        + "("
        + dstIP
        + ")."
    )
    command = [
        "logpostman",
        "--spoof",
        srcIP,
        "--eps",
        250,
        "-file",
        os.path.abspath(fpath),
        "--quiet",
        "--raw",
        dstIP,
    ]
    subprocess.call(command)
    print(
        "Transmission from spoof "
        + os.path.basename(fpath).split(",")[0].split("to")[0]
        + "("
        + srcIP
        + ") to "
        + os.path.basename(fpath).split(",")[0].split("to")[1]
        + "("
        + dstIP
        + ") completed."
    )


if __name__ == "__main__":
    lists = []
    args = sys.argv
    for i in range(1, 1, len(args)):
        lists.append(args[i])
    with multiprocessing.Pool(processes=NUMBER_OF_TASKS) as p:
        p.map(work, lists)

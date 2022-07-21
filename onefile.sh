#!/usr/bin/env bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install scapy
pip install pyinstaller
pyinstaller --onefile logpostman.py
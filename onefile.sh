#!/usr/bin/env bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install scapy
pip install pyinstaller
mkdir -p ./work
cp logpostman.py ./work
cd ./work
pyinstaller --onefile logpostman.py
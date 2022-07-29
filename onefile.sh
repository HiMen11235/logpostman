#!/usr/bin/env bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install scapy
pip install pyinstaller
pip install staticx
pip install patchelf-wrapper
mkdir -p ./work
cp logpostman.py ./work
cd ./work
pyinstaller --onefile logpostman.py
mv dist/logpostman dist/logpostman.old
staticx dist/logpostman.old dist/logpostman
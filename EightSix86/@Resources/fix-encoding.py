#!/usr/bin/env python3
"""
Re-stamp every EightSix86/**/*.ini and *.inc as UTF-8 with BOM.

Why: Rainmeter on a Chinese-locale Windows reads INI files as GBK by default.
Files saved as plain UTF-8 will mojibake any non-ASCII char (▶ → 钰?, · → 路).
A leading UTF-8 BOM (EF BB BF) tells Rainmeter to use UTF-8 instead.

Run this every time you've edited a skin file with a tool that strips the BOM
(most macOS/Linux editors and any Write/Edit tool do).

Usage:
    cd /path/to/MyRainmeterSkin
    python3 EightSix86/@Resources/fix-encoding.py
"""
import codecs
import glob
import os
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(repo_root)

files = sorted(set(
    glob.glob('EightSix86/**/*.ini', recursive=True) +
    glob.glob('EightSix86/**/*.inc', recursive=True)
))

count = 0
for f in files:
    with open(f, 'rb') as fp:
        data = fp.read()

    if data.startswith(codecs.BOM_UTF8):
        text = data[3:].decode('utf-8')
        had = 'utf8-bom'
    elif data.startswith(codecs.BOM_UTF16_LE):
        text = data[2:].decode('utf-16-le')
        had = 'utf16-le-bom'
    elif data.startswith(codecs.BOM_UTF16_BE):
        text = data[2:].decode('utf-16-be')
        had = 'utf16-be-bom'
    else:
        try:
            text = data.decode('utf-8')
            had = 'utf8-no-bom'
        except UnicodeDecodeError:
            text = data.decode('utf-16-le')
            had = 'utf16-le-no-bom'

    with open(f, 'wb') as fp:
        fp.write(codecs.BOM_UTF8)
        fp.write(text.encode('utf-8'))

    print(f'{had:18s} -> utf8-bom  {f}')
    count += 1

print(f'\n{count} file(s) re-stamped as UTF-8 with BOM.')

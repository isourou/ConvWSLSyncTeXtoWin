#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2021 Kentaro Iwami.
# This file is part of ConvSyncTeXtoWin, distributed under the terms of the
# Boost Software License - Version 1.0.  See the accompanying
# LICENSE file or <http://www.boost.org/LICENSE_1_0.txt>import os

import os
import gzip
import subprocess
import sys

argc = len(sys.argv)
print(argc)
if (argc != 2):
    print("Usage: > python "+sys.argv[0]+" %DOCFILE%")
    quit(0)

docfile = sys.argv[1]

if os.path.exists("./"+docfile+".synctex.gz"):
    print ("./"+docfile+".synctex.gz found.")
    encode = True
    with gzip.open("./"+docfile+".synctex.gz", "rt", encoding="utf_8", newline='\n') as fi:
        text = fi.readlines()
elif os.path.exists("./"+docfile+".synctex"):
    print ("./"+docfile+".synctex found.")
    encode = False
    with open("./"+docfile+".synctex", "r", encoding="utf_8", newline='\n') as fi:
        text = fi.readlines()
else:
    print("File not found.")
    quit(0)

outlist = list()
for line in text:
    if ("Input" in line):
        dummy, num, path = line.split(':',2)
        cp = subprocess.run(['wsl', 'wslpath', '-w', path], encoding='utf-8', stdout=subprocess.PIPE)
        if cp.returncode == 0: 
            if cp.stdout[1]== ":":
                drive, path2 = cp.stdout.split(':',1)
                lowdrive = drive.lower()
                newpath = lowdrive+":"+path2
            else :
                newpath = cp.stdout
            buf = "Input:"+num+":"+newpath
            outlist.append(buf)
            print(buf)
    else:
        outlist.append(line)

# 改行コードはLFじゃないとだめ
if encode is True:
    with gzip.open("./"+docfile+".synctex.gz", "wt", encoding="utf_8", newline='\n') as fo:
        fo.writelines(outlist)
else:
    with open("./"+docfile+".synctex", "w", encoding="utf_8", newline='\n') as fo:
        fo.writelines(outlist)


# ConvWSLSyncTeXtoWin
This script converts .synctex or .synctex.gz file generated by (La)TeX on WSL to Windows format 

# Introduction
TeX compile on WSL is very fast compared to TeX Live for Windows, especially for long (~100 pages) Japanese format.
However, as the geneated *.synctex or *.synctex.gz file is based on WSL file path format, it does not work well on Windows, for example VSCode + Latex Workshop internal viewer or VSCode + SmatraPDF.

# How to install
Put ConvWSLSyncTeXtoWin.py to the same folder with the root .tex file. 
Add the following entry to settings.json file of VSCode.

``` settings.json

"latex-workshop.latex.tools": [
  //WSLでコンパイルしたSyncTeXをWindows形式に変換
  {
    "name": "convwslsynctextowin",
    "command": "python",
    "args": [
      "ConvWSLSyncTeXtoWin.py", "%DOCFILE%"
    ]
  }

// 使いたいレシピのtoolsの最後(dvipdfmxの後ろ)に"convwslsynctextowin"を追加する
"latex-workshop.latex.recipes": [
  {
    "name": "build_thesis",
    "tools": [
       "upLaTeX","hoge","fuga","foo","bar","dvipdfmx","convwslsynctextowin"
    ]
  },
```

``` ConvWSLSyncTeXtoWin.py 

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
```
 

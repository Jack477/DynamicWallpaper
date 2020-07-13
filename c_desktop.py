#!/usr/bin/python
import os 
import sys
import subprocess as sp
dir_path = os.path.dirname(os.path.realpath(__file__))
f_content = '[Desktop Entry]\nName=DynamicWallpaper\nComment=App for change wallpaper\nExec='+sys.argv[1]+'/Backgrounds/start.sh\nIcon='+sys.argv[1]+'/Backgrounds/icon.png\nCategories=Utility;\nVersion=1.0\nType=Application\nTerminal=false\nStartupNotify=true'
d_dir = sys.argv[1]+"/Desktop/dynamicwallpaper.desktop"
x_dir = "/usr/share/applications/dynamicwallpaper.desktop"
print(d_dir)
f = open(d_dir, "w+")
f.write(f_content)
f.close
f2 = open(x_dir, "w+")
f2.write(f_content)
f2.close

#!/usr/bin/python3
import sys
import os
def set_rc(x):
	print(x)
	rc_path = "/etc/rc.local"
	num_lines = sum(1 for line in open(rc_path))
	fin = open(rc_path, 'r')
	lines = fin.readlines()
	if x == 'T':
		print("setting up in rc.local")
		lines[-2] = sys.argv[2]+"/Backgrounds/change_theme.py &\n"
	if x == 'F':
		print("disable rc.local")
		if "change_theme" in lines[-2]:
			lines[-2] = "\n"
	open(rc_path, 'w').writelines(lines)
set_rc(sys.argv[1])

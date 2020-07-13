#!/usr/bin/python3
# TODO:
# 1. move /Backgrounds into /usr/share/backgrounds
# 2. !DONE use user variable ${HOME} to get path and rewrite all paths
# 3. !DONE configure cron to run script on specify hours
# 4. !DONE MAKE GUI!
# 5. finish logical layer of this app
# 5a. add/remove stuff from /etc/rc.local
# 6. some config in future? configparser could be usefull


# COMMANDS
#sudo -H -u pi bash -c 'python3 wallpaper.py'
#xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s /home/pi/Backgrounds/main/xwallpaper.jpg


import os
import datetime
import configparser
import tkinter as tk
import subprocess as sp
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from os.path import expanduser
from tkinter import messagebox as msb

user_path = expanduser("~")

print(user_path)
sys_date = datetime.datetime.now().time()
#print(sys_date.hour)

### List of all images as arrays
BigSur = ["BigSur2.jpg", "BigSur3.jpg", "BigSur4.jpg", "BigSur5.jpg", "BigSur6.jpg", "BigSur7.jpg", "BigSur8.jpg", "BigSur1.jpg"]
Catalina = ["Catalina2.jpg", "Catalina3.jpg", "Catalina4.jpg", "Catalina5.jpg", "Catalina6.jpg", "Catalina7.jpg", "Catalina8.jpg", "Catalina1.jpg"]
Mojave = ["Mojave2.jpg", "Mojave3.jpg", "Mojave4.jpg", "Mojave5.jpg", "Mojave6.jpg", "Mojave7.jpg", "Mojave8.jpg", "Mojave1.jpg"]



config = configparser.ConfigParser()
if os.path.exists('Backgrounds/bg.config'):
	config.read('Backgrounds/bg.config')
	print("Exist and read")
else:
	print("Creating config...")
	config['DEFAULT'] = {'wallpaper': '0'}
	with open(user_path+'/Backgrounds/bg.config', 'w+') as configfile:
		config.write(configfile)


def set_enable(xvar):
	autostartsetup=False
	cronsetup=False
	crontext = sp.getoutput('crontab -l')
	autostart = open("/etc/rc.local", 'r')
	autostart_data = autostart.read()
	if "change_theme" in autostart_data:
		autostartsetup=True
		print("I found change_theme.py in autostart setup!")
	if "change_theme" in crontext:
		cronsetup=True
		print("I found change_theme.py!")
		
	print(cronsetup)
	print(autostartsetup)
	
	if cronsetup==True and xvar.get()==1:
		print("Dont change crontable bc it's already enabled")
	if cronsetup==False and xvar.get()==1:
		os.system('crontab -l | { cat; echo "0 * * * * sudo -H -u pi bash -c \'python3 Backgrounds/change_theme.py\' >> /home/pi/wallpaper_log.txt"; } | crontab -')
		os.system('sudo python3 '+user_path+'/Backgrounds/rc.py T '+user_path)
		#rc.set_rc(True)
		#os.system('sudo sed -i "`wc -l < /etc/rc.local`i\\sudo python3 /home/pi/Backgrounds/change_theme.py &\\" /etc/rc.local')
		os.system('sudo service cron restart')
		os.system('xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s ${HOME}/Backgrounds/main/xwallpaper.jpg')
		print("Setup crontab...")
	if cronsetup==True and xvar.get()==0:
		print("Removing")
		os.system('crontab -l | grep -v \'change_theme\' | crontab -')
		os.system('sudo service cron restart')
		os.system('sudo python3 '+user_path+'/Backgrounds/rc.py F')
		os.system('sudo sed -i \'s/sudo python3.*//\' /etc/rc.local')
		os.system('xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s /usr/share/rpd-wallpaper/raspbian-x-nighthawk.png')
		print("Removing from crontab...")
	if cronsetup==False and xvar.get()==0:
		print("Nothing changed bc it's already disable")
		
def push(xvar, zvar):
	print(xvar.get())
	print(zvar.get())
	set_enable(xvar)
	config.set('DEFAULT', 'wallpaper', str(zvar.get()))
	with open('Backgrounds/bg.config', 'w') as configfile:
		config.write(configfile)
	if xvar.get() == 1:
		os.system('python3 Backgrounds/change_theme.py')
	
class Window:

	def __init__(master):
		

		master = tk.Tk()
		
		var = IntVar()
		var2= IntVar()
		p1=False
		p2=False
		master.geometry("800x450")
		master.title("Wallpaper")

		mainframe = Frame(master)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
		
		title_label = tk.Label(titleframe, text="Dynamic Wallpaper", font=("TkDefaultFont", 11, "bold"))
		title_label.pack(side=LEFT)
		
		radioframe = Frame(mainframe)
		radioframe.pack(fill=X, pady=15)
		
		option_enable = Radiobutton(radioframe, text="Enable", variable=var, value=1)
		option_enable.pack(side=LEFT)
		
		option_disable = Radiobutton(radioframe, text="Disable", variable=var, value=0)
		option_disable.pack(side=LEFT)
		
		wallpaperframe=Frame(mainframe, bg="White", highlightthickness=1, highlightbackground="gray")
		wallpaperframe.pack(fill=X)
		
		

		
		BigSurLabel = tk.Label(wallpaperframe, text="BigSur", font=("TkDefaultFont", 11, "bold"), bg="White")
		BigSurLabel.grid(row=0, column=0, pady=10)
		
		loadimg = Image.open(user_path+"/Backgrounds/preview/BigSurPreview.png")
		img = ImageTk.PhotoImage(image=loadimg)       
		img_label = tk.Label ( wallpaperframe, image=img, bg="White")
		
		img_label.image = img
		img_label.grid(row=1, column=0, padx=15)
		
		option_BigSur = Radiobutton(wallpaperframe, variable=var2, value=1,  bg="White")
		option_BigSur.grid(row=2, column=0, pady=10)
		option_BigSur.select()
		
		CatalinaLabel = tk.Label(wallpaperframe, text="Catalina", font=("TkDefaultFont", 11, "bold"), bg="White")
		CatalinaLabel.grid(row=0, column=1, pady=10)
		
		loadimg2 = Image.open(user_path+"/Backgrounds/preview/CatalinaPreview.png")
		img2 = ImageTk.PhotoImage(image=loadimg2)       
		img_label2 = tk.Label ( wallpaperframe, image=img2, bg="White")
		
		img_label2.image = img2
		img_label2.grid(row=1, column=1, padx=15)
		
		option_Catalina = Radiobutton(wallpaperframe, variable=var2, value=2, bg="White")
		option_Catalina.grid(row=2, column=1, pady=10)
		
		
		
		MojaveLabel = tk.Label(wallpaperframe, text="Mojave", font=("TkDefaultFont", 11, "bold"), bg="White")
		MojaveLabel.grid(row=0, column=2, pady=10)
		
		loadimg3 = Image.open(user_path+"/Backgrounds/preview/MojavePreview.png")
		img3 = ImageTk.PhotoImage(image=loadimg3)       
		img_label3 = tk.Label ( wallpaperframe, image=img3, bg="White")
		
		img_label3.image = img3
		img_label3.grid(row=1, column=2, padx=15)
		
		option_Mojave = Radiobutton(wallpaperframe, variable=var2, value=3, bg="White")
		option_Mojave.grid(row=2, column=2, pady=10)
		#photo2 = PhotoImage(file = r""+user_path+"/Backgrounds/preview/CatalinaPreview.png") 
		#option_Catalina = Radiobutton(wallpaperframe, text="Catalina", variable=var2, value=2, #command=switch_wallpaper, font=("TkDefaultFont", 11, "bold"), compound=TOP, image=photo2)
		#option_Catalina.pack(side=LEFT,padx=10, pady=5)
		
		#photo3 = PhotoImage(file = r""+user_path+"/Backgrounds/preview/MojavePreview.png") 
		#option_Mojave = Radiobutton(wallpaperframe,  variable=var2, value=3, command=switch_wallpaper, font=("TkDefaultFont", 11, "bold"), text="Mojave", image=photo3, compound=TOP)
		#option_Mojave.pack(side=LEFT, padx=10, pady=5)
		
		wButton = Button(mainframe, text="Save and Close", bg="#2866F8", fg="White", font=("TkDefaultFont", 11, "bold"), cursor="hand2", activebackground="Blue", activeforeground="White", command=lambda:push(var, var2))
		wButton.pack(anchor='e', pady=30)
		master.mainloop()	
		
		
def main():
	start = Window()
	
	
if __name__ == '__main__':
    main()
#!/usr/bin/python3
import os
import subprocess
import datetime
import ephem
import wallpaper as wp
from os.path import expanduser
from datetime import datetime

xwallpaper= wp.config['DEFAULT']['wallpaper']
user_path = expanduser("~")

### List of all images as arrays
BigSur = ["BigSur2.jpg", "BigSur3.jpg", "BigSur4.jpg", "BigSur5.jpg", "BigSur6.jpg", "BigSur7.jpg", "BigSur8.jpg", "BigSur1.jpg"]
Catalina = ["Catalina2.jpg", "Catalina3.jpg", "Catalina4.jpg", "Catalina5.jpg", "Catalina6.jpg", "Catalina7.jpg", "Catalina8.jpg", "Catalina1.jpg"]
Mojave = ["Mojave2.jpg", "Mojave3.jpg", "Mojave4.jpg", "Mojave5.jpg", "Mojave6.jpg", "Mojave7.jpg", "Mojave8.jpg", "Mojave1.jpg"]

### Function to convert ephem Date type to timecode that represents time of day in minutes
def get_code(aDate) : 
	tm = aDate.tuple()
	return (datetime(*tm[0:5]).hour * 60) + datetime(*tm[0:5]).minute

### Function to set selected images as a wallpaper
def set_theme(theme):
	xdir = theme[:-5]
#	print(xdir)
	print("Setting up theme as "+str(theme))
	# Suppressing console output for copy operations, but leave for desktop reload...
	with open(os.devnull, 'wb') as devnull:
		subprocess.check_call(['rm', '-f', user_path+'/Backgrounds/main/xwallpaper.jpg'], stdout=devnull, stderr=subprocess.STDOUT)
		subprocess.check_call(['cp', user_path+'/Backgrounds/'+xdir+'/'+theme, user_path+'/Backgrounds/main/xwallpaper.jpg'], stdout=devnull, stderr=subprocess.STDOUT)
		os.system('export DISPLAY=:0.0')
		print('Reloading desktop...')
		subprocess.check_call(['xfdesktop', '-reload'])
	devnull.close()

### Function to calculate a part of day and make a decision what image should be selected
def f(images):
	defLoc = False
	if not (wp.config.has_option('DEFAULT', 'location') ):
		defLoc = True
	elif (wp.config['DEFAULT']['location'] == 'default' ):
		defLoc = True
	else :
		defLoc = False
	if defLoc :
		t_beg_civ = 6 * 60
		t_sunrise = 8 * 60
		t_morning = 10 * 60
		t_noon    = 16 * 60
		t_evening = 18 * 60
		t_sunset  = 19 * 60
		t_end_civ = 20 * 60
		t_dark    = 21 * 60
	else :
		#Make an observer
		geo = ephem.Observer()
		
		#PyEphem takes and returns only UTC times. Select 12:00 as midday for further calculations
		geo.date = datetime.utcnow().replace(hour = 12, minute = 0, second = 0)
		
		#Location of desired place is taken from settings file
		geo.lon  = wp.config['DEFAULT']['lon'] #Note that lon should be in string format
		geo.lat  = wp.config['DEFAULT']['lat'] #Note that lat should be in string format
	
		print('Calculating day parts for lat: '+wp.config['DEFAULT']['lat']+' lon: '+wp.config['DEFAULT']['lon']+'...')
	
		#Take some elevation above ground, 20 meters for now...
		geo.elev = 20
		
		#To get U.S. Naval Astronomical Almanac values, use these settings
		geo.pressure= 0
		geo.horizon = '-0:34'
		
		# As for some polar regions some Sun transitions are not reachable.
		# So, a try ... except blocks are organized with some preset values:
		# Wallpaper change at: 06:00 08:00 10:00 16:00 18:00 19:00 20:00 21:00
		try:
			sunrise=geo.previous_rising(ephem.Sun()) #Sunrise
		except	ephem.NeverUpError : 
			sunrise=ephem.Date(1500 + 8 * ephem.hour + 00 * ephem.minute)
		t_sunrise = get_code(sunrise)
		
		try:
			noon   =geo.next_transit   (ephem.Sun(), start=sunrise) #Solar noon
		except	ephem.NeverUpError : 
			noon=ephem.Date(1500 + 18 * ephem.hour + 00 * ephem.minute)
		t_noon = get_code(noon)
		
		try:
			sunset =geo.next_setting   (ephem.Sun()) #Sunset
		except	ephem.NeverUpError : 
			sunset=ephem.Date(1500 + 19 * ephem.hour + 00 * ephem.minute)
		t_sunset = get_code(sunset)
		
		# Relocate the horizon to get twilight times
		geo.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
	
		try:
			beg_civ=geo.previous_rising(ephem.Sun(), use_center=True) #Begin civil twilight
		except	ephem.NeverUpError : 
			beg_civ=ephem.Date(1500 + 6 * ephem.hour + 00 * ephem.minute)
		t_beg_civ = get_code(beg_civ)
		
		try:
			end_civ=geo.next_setting   (ephem.Sun(), use_center=True) #End civil twilight
		except	ephem.NeverUpError : 
			end_civ=ephem.Date(1500 + 20 * ephem.hour + 00 * ephem.minute)
		t_end_civ = get_code(end_civ)
		
		# Relocate the horizon to get morning / evening times, maybe 5 degrees above ground is too much
		geo.horizon = '5' #-6=civil twilight, -12=nautical, -18=astronomical
	
		try:
			morning=geo.previous_rising(ephem.Sun(), use_center=True) #Begin civil twilight
		except	ephem.NeverUpError : 
			morning=ephem.Date(1500 + 10 * ephem.hour + 00 * ephem.minute)
		t_morning = get_code(morning)
		
		try:
			evening=geo.next_setting   (ephem.Sun(), use_center=True) #End civil twilight
		except	ephem.NeverUpError : 
			evening=ephem.Date(1500 + 19 * ephem.hour + 00 * ephem.minute)
		t_evening = get_code(evening)
		
		# Relocate the horizon to get nautical twilight
		geo.horizon = '-12' #-6=civil twilight, -12=nautical, -18=astronomical
		try:
			dark=geo.next_setting   (ephem.Sun(), use_center=True) #End civil twilight
		except	ephem.NeverUpError : 
			dark=ephem.Date(1500 + 21 * ephem.hour + 00 * ephem.minute)
		t_dark = get_code(dark)
	
		# All calculations are made, lets decide what part of day is now.
		# Again, times _MUST_ be in UTC
		geo.date = datetime.utcnow()
		
		# Debug output for calculated transitions
		print(geo.date, '<-- UTC its now code -->', get_code(geo.date))
	
		print('\n',
			'0 ', beg_civ, t_beg_civ, '\n',
			'1 ', sunrise, t_sunrise, '\n',
			'2 ', morning, t_morning, '\n',
			'3 ', noon,    t_noon,    '\n',
			'4 ', evening, t_evening, '\n',
			'5 ', sunset,  t_sunset,  '\n',
			'6 ', end_civ, t_end_civ, '\n',
			'7 ', dark,    t_dark, '   \n')

	# Convert current time to timecode
	if defLoc : t_curr = datetime.now().hour*60
	else :      t_curr = get_code(geo.date)

	# And make final decision with theme setting.
	if   ( (t_curr >= t_beg_civ) and (t_curr < t_sunrise) ):
		set_theme(images[0])
		print('0 - Twilight sunrise, next in', t_sunrise-t_curr, 'minutes.')
	
	elif ( (t_curr >= t_sunrise) and (t_curr < t_morning) ):
		set_theme(images[1])
		print('1 - Sunrise, next in', t_morning-t_curr, 'minutes.')
	
	elif ( (t_curr >= t_morning) and (t_curr < t_noon)    ):
		set_theme(images[2])
		print('2 - Morning, next in', t_noon-t_curr, 'minutes.')
	
	elif ((t_curr >= t_noon)     and (t_curr < t_evening) ):
		set_theme(images[3])
		print('3 - Noon, next in', t_evening-t_curr, 'minutes')
	
	elif ((t_curr >= t_evening)  and (t_curr < t_sunset)  ):
		set_theme(images[4])
		print('4 - Evening, next in', t_sunset-t_curr, 'minutes.')
	
	elif ( (t_curr >= t_sunset)  and (t_curr < t_end_civ) ):
		set_theme(images[5])
		print('5 - Sunset, next in', t_end_civ-t_curr, 'minutes.')
	
	elif ( (t_curr >= t_end_civ) and (t_curr < t_dark)    ):
		set_theme(images[6])
		print('6 - Twilight sunset, next in', t_dark-t_curr, 'minutes.')
	
	else :
		set_theme(images[7])
		print('7 - Night...' )

## main script
if int(xwallpaper)==1:
	f(BigSur)
if int(xwallpaper)==2:
	f(Catalina)
if int(xwallpaper)==3:
	f(Mojave)
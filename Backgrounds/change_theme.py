#!/usr/bin/python3
import os
import datetime
from datetime import datetime
import ephem
import wallpaper as wp
from os.path import expanduser

xwallpaper=wp.config['DEFAULT']['wallpaper']
user_path = expanduser("~")

### List of all images as arrays
BigSur = ["BigSur2.jpg", "BigSur3.jpg", "BigSur4.jpg", "BigSur5.jpg", "BigSur6.jpg", "BigSur7.jpg", "BigSur8.jpg", "BigSur1.jpg"]
Catalina = ["Catalina2.jpg", "Catalina3.jpg", "Catalina4.jpg", "Catalina5.jpg", "Catalina6.jpg", "Catalina7.jpg", "Catalina8.jpg", "Catalina1.jpg"]
Mojave = ["Mojave2.jpg", "Mojave3.jpg", "Mojave4.jpg", "Mojave5.jpg", "Mojave6.jpg", "Mojave7.jpg", "Mojave8.jpg", "Mojave1.jpg"]

def get_code(aDate) : 
	tm = aDate.tuple()
	return (datetime(*tm[0:5]).hour * 10) + datetime(*tm[0:5]).minute

def set_theme(theme):

	xdir = theme[:-5]
#	print(xdir)
	print("Setting up theme as "+str(theme))
	os.system('rm '+user_path+'/Backgrounds/main/xwallpaper.jpg')
	os.system('cp '+user_path+'/Backgrounds/'+xdir+'/'+theme+' '+user_path+'/Backgrounds/main/xwallpaper.jpg')
	os.system('export DISPLAY=:0.0')
	print('Reloading desktop...')
	os.system('xfdesktop -reload')
	
def f(images):
	#Make an observer
	geo      = ephem.Observer()
	
	#PyEphem takes and returns only UTC times. 15:00 is noon in Fredericton
	geo.date = datetime.utcnow().replace(hour = 12, minute = 0, second = 0)
	
	#Location of 
	geo.lon  = wp.config['DEFAULT']['lon'] #Note that lon should be in string format
	geo.lat  = wp.config['DEFAULT']['lat'] #Note that lat should be in string format
	print('Calculating day parts for lat: '+wp.config['DEFAULT']['lat']+' lon: '+wp.config['DEFAULT']['lon']+'...')
	#Elevation of Fredericton, Canada, in metres
	geo.elev = 20
	
	#To get U.S. Naval Astronomical Almanac values, use these settings
	geo.pressure= 0
	geo.horizon = '-0:34'
	
	try:
		sunrise=geo.previous_rising(ephem.Sun()) #Sunrise
	except	ephem.NeverUpError : 
		sunrise=ephem.Date(1500 + 8 * ephem.hour + 00 * ephem.minute)
	
	try:
		noon   =geo.next_transit   (ephem.Sun(), start=sunrise) #Solar noon
	except	ephem.NeverUpError : 
		noon=ephem.Date(1500 + 18 * ephem.hour + 00 * ephem.minute)
	
	try:
		sunset =geo.next_setting   (ephem.Sun()) #Sunset
	except	ephem.NeverUpError : 
		sunset=ephem.Date(1500 + 19 * ephem.hour + 00 * ephem.minute)
	
	#We relocate the horizon to get twilight times
	geo.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
	
	try:
		beg_civ=geo.previous_rising(ephem.Sun(), use_center=True) #Begin civil twilight
	except	ephem.NeverUpError : 
		beg_civ=ephem.Date(1500 + 6 * ephem.hour + 00 * ephem.minute)
	
	try:
		end_civ=geo.next_setting   (ephem.Sun(), use_center=True) #End civil twilight
	except	ephem.NeverUpError : 
		end_civ=ephem.Date(1500 + 20 * ephem.hour + 00 * ephem.minute)
	
	geo.horizon = '5' #-6=civil twilight, -12=nautical, -18=astronomical
	
	try:
		morning=geo.previous_rising(ephem.Sun(), use_center=True) #Begin civil twilight
	except	ephem.NeverUpError : 
		morning=ephem.Date(1500 + 10 * ephem.hour + 00 * ephem.minute)
	
	try:
		evening=geo.next_setting   (ephem.Sun(), use_center=True) #End civil twilight
	except	ephem.NeverUpError : 
		evening=ephem.Date(1500 + 19 * ephem.hour + 00 * ephem.minute)
	
	geo.horizon = '-12' #-6=civil twilight, -12=nautical, -18=astronomical
	try:
		dusk=geo.next_setting   (ephem.Sun(), use_center=True) #End civil twilight
	except	ephem.NeverUpError : 
		dusk=ephem.Date(1500 + 21 * ephem.hour + 00 * ephem.minute)
	
	geo.date = datetime.utcnow()
	
	print(geo.date, ' <-- its now in UTC')
	print('\n', '0 ', beg_civ, '\n', '1 ', sunrise, '\n', '2 ', morning, '\n', '3 ', noon, '\n', '4 ', evening, '\n', '5 ', sunset, '\n', '6 ', end_civ, '\n', '7 ', dusk, '\n')
	
	curr = get_code(geo.date)
	
	print(curr, ' <-- its now in datecode')
	
	if ( (curr >= get_code(beg_civ)) and (curr < get_code(sunrise)) ):
		set_theme(images[0])
		print('0 - Twilight sunrise')
	elif ( (curr >= get_code(sunrise)) and (curr < get_code(morning)) ):
		set_theme(images[1])
		print('1 - Sunrise')
	elif ( (curr >= get_code(morning)) and (curr < get_code(noon)) ):
		set_theme(images[2])
		print('2 - Morning')
	elif ((curr >= get_code(noon)) and (geo.date < get_code(evening) )):
		set_theme(images[3])
		print('3 - Noon')
	elif ((curr >= get_code(evening)) and (geo.date < get_code(sunset)) ):
		set_theme(images[4])
		print('4 - Evening')
	elif ( (curr >= get_code(sunset)) and (geo.date < get_code(end_civ)) ):
		set_theme(images[5])
		print('5 - Sunset')
	elif ( (curr >= get_code(end_civ)) and (geo.date < get_code(dusk)) ):
		set_theme(images[6])
		print('6 - Twilight sunset')
	else :
		set_theme(images[7])
		print('7 - Night')

if int(xwallpaper)==1:
	f(BigSur)
if int(xwallpaper)==2:
	f(Catalina)
if int(xwallpaper)==3:
	f(Mojave)
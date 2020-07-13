#!/bin/bash
xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s ${HOME}/Backgrounds/main/xwallpaper.jpg
#crontab -l | { cat; echo "0 * * * * sudo -H -u pi bash -c 'python3 wallpaper.py' >> /home/pi/wallpaper_log.txt"; } | crontab -
#sudo sed -i "`wc -l < /etc/rc.local`i\\sudo python3 /home/pi/Backgrounds/change_theme.py &\\" /etc/rc.local
problem=$(dpkg -s python3-tk|grep installed)
echo Checking for tkinter: $problem
if [ "" == "$problem" ]; then
	sudo apt-get install python3-tk
fi
sudo apt-get install python3-pil python3-pil.imagetk
sudo python3 c_desktop.py ${HOME}
sudo chmod +x ${HOME}/Backgrounds/start.sh
sudo chmod +x ${HOME}/Desktop/dynamicwallpaper.desktop
sudo rm ${HOME}/c_desktop.py

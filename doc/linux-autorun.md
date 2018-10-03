### TL;DR
 (*)

### Operating System
This is for Linux only

### Purpose
To execute KrakenX script inside a service daemon that gets launched during boot up.

This is very important so you don't have to remember to always run the script after you log in.

With CAM on Windows, everything kicks in when Windows boots up. On Linux however, NZXT provides no driver support or CAM. When Linux boots up, your Kraken AIO will default to a white RGB pump header color and the fans and pump will operate at default settings.

If you want more control than this. KrakenX lets you change this.

What follows are instructions on how to get the latest KrakenX script, install all relevant code, configure your Kraken liquid cooler and administrate the auto run service.

### Get Python and PIP Assets, Setup and Install

sudo apt install python3
sudo apt-get install python3-usb
sudo apt-get install python3-pip

### Get KrakenX Assets, Setup and Install

cd /etc
mkdir colctl
Download Kraken Zip file and copy to /etc/colctl
unzip krakenx-master.zip
cd krakenx-master
python3 -m pip install krakenx (don't sudo or file error with owner cache permission appears)

**Verify Your File Structure**

Before you proceed, make sure your file structure looks similar to this:

/etc
--/colctl
------colctl
--/krakenx
-----color_change.py
-----__init__.py
-----profile.py

These are the minimal folder and files you need to run KrakenX. They must be in this layout or the auto run service will not work.

### Create a System Daemon Service For KrakenX
This involves running a text editor (nano in this case) to type some stuff in. You will save the text file in /etc/systemd/service under the filename krakenx.service. 

The parameter settings below are set for (*):
- SpectrumWave RGB on the pump header
- Fan speed (Celcius, not Fahrenheit):
    Above 20C at 25% level
    Above 30C at 60% level
    Above 40C at 80% level
    Above 50C at 100% level
- Pump speed
    Above 20C at 60% level
    Above 30C at 70% level
    Above 40C at 80% level
    Above 50C at 100% level

Adjust the above to your liking.

cd /etc/systemd/service
sudo nano krakenx.service

[Unit]
Description=Kraken AIO startup service

[Service]
Type=oneshot
User=root
WorkingDirectory=/etc/colctl
ExecStart=/etc/colctl/colctl --mode SpectrumWave --fan_speed "(20,25),(30,60),(40,80),(50,100)" --pump_speed "(20,60),(30,70),(40,80),(50,100)"

[Install]
WantedBy=multi-user.target

### Set Permissions and Ownership

sudo chmod 644 krakenx.service (must be 644 or syslog will show errors)
sudo chown root:root krakenx.service
chmod 755 /etc/colctl/colctl
chown root:root /etc/colctl/colctl

### Using KrakenX Service

Ready? Set. Go!

This first command starts the service and puts it in running state.
The second command enables it so that on next boot, it will run automatically.

sudo systemctl start krakenx.service
sudo systemctl enable krakenx.service

You should now see your Kraken RGB, fans, and pump run at your specified settings.

### Other Things You May Need To Know

These are things that you may need to use later to administrate the service. If you make changes to any of the parameter settings above, you need to stop the service, update systemd, and restart the service again.

I leave them here for reference.

**_To start the service_**
systemctl start krakenx.service
systemctl enable krakenx.service
	
**_To stop the service_**
systemctl stop krakenx.service
systemctl disable krakenx.service

**_To restart the service_**
systemctl restart kraken.service
	
**_To reload the service_**
systemctl reload krakenx.service
	
**_To restart and reload the service_**
systemctl reload-or-restart krakenx.service
	
**_To remove the service_**
systemctl stop krakenx.service
systemctl disable krakenx.service
rm /etc/systemd/system/krakenx.service
rm /etc/systemd/system/krakenx.service (don't forget symlinks)

**_To update systemd_**
systemctl daemon-reload
systemctl reset-failed
	
**_Status, targets and properties_**
systemctl get-default or ls -al /lib/systemd/system/default.target
ls -al /lib/systemd/system/runlevel*
systemctl list-unit-files
systemctl list-units --type=target
systemctl is-enabled krakenx.service
systemctl is-failed krakenx.service
systemctl is-active krakenx.service
systemctl show krakenx.service

Hope this helps someone. Feel free to add to the project README.

Note: This was edited several times to arrive at this solution. I do not recommend using cron or setting colctl in shell startup scripts. I had problems getting them to work. This is much cleaner, set and forget solution.

**_(*) Use at your own risk. I will not be held responsible for anything that may go wrong. This was developed and tested on Ubuntu 18.0.4 desktop._**
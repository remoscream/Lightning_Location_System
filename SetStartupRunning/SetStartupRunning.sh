# Shell script for set up boot-up running of run.sh
# This script only run the commands from step 3 to 5 (README.md)
# You can copy RunLLS.service in the folder to /lib/systemd/system/ the run this script

sudo chmod 744 /home/pi/Lightning_Location_System/run.sh
sudo chmod 664 /lib/systemd/system/RunLLS.service
sudo systemctl daemon-reload
sudo systemctl enable systemd-networkd
sudo systemctl enable RunLLS.service
sudo reboot
# Script for delete all data files
read -p "This program will delete all data files, are you really sure? [Y/N] : " judge

if judge="Y"; then
  sudo rm -f /home/pi/Lightning_Location_System/data_bme280/*
  sudo rm -f /home/pi/Lightning_Location_System/data_condition/*
  sudo rm -f /home/pi/Lightning_Location_System/data_as3935/*
fi


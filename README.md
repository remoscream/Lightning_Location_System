# Table of Contents
- [Background](#Shell-Scripts)
- [2. Initialization](#)
- []()
- []()
- []()

## Background


## Initialization ([CommonParameters.py](./CommonParameters.py))
- This script saves parameters that may be usually changed for convenience in this LLS project.

  __(Be attention, this script not contains all parameters of each sensor like BME280 has so many parameters for different environments. If you can not find the parameters that written on the datasheets of the sensors, please check them in the program of each module, especially the files with a head of `Rpi_`.)__

- This script has been imported as `cp` in the program of each module.
- Before using this script to set up your system, I highly recommend you to read the datasheets related to this project.Here is a list of datasheets I suggest you to read :
  - [AS3935](https://datasheetspdf.com/datasheet/AS3935.html)
  - [AS3935 module (Japanese)](https://akizukidenshi.com/catalog/g/gK-08685/) 
  - [BME280](https://www.datasheets.com/en/part-details/bme280-bosch-67258952#datasheet)
  - [BME280 module (Japanese)](https://akizukidenshi.com/catalog/g/gK-09421/) 
  - [MT3333](https://www.datasheets.com/en/part-details/mt3333av-mediatek-424168090#datasheet)
  - [GNSS module (Japanese)](https://akizukidenshi.com/catalog/g/gK-13850/) 
  - [PCA9600](https://www.datasheets.com/en/part-details/pca9600d-nxp-semiconductors-42660407#datasheet)


##Lightning Sensor Module
### 1. [AS3935.py](./AS3935.py)
The main program for AS3935. This program is referenced from the website below :
- [Ishikawa-lab (Japanese)](https://www.ishikawa-lab.com/RasPi_lightning.html)

The packages you need is list below: 
```
sudo apt -y install i2c-tools
sudo pip3 install smbus
sudo pip3 install RPi.GPIO
sudo apt -y install python3-numpy
```
As we often need to adjust the parameters `WDTH` and `SREJ` for different electromagnetic environments, so I not use `pip3 install RPi_AS3935` but download from pypi and modified it for adjust `WDTD` and `SREJ` more easily.
- [Original RPi_AS3935.py (pypi)](https://pypi.org/project/RPi_AS3935/)

Therefore, you should use `RPi_AS3935.py` in this repository for this project.

### 2. [AS3935_Calibration.py](./AS3935_Calibration.py)
This program is based this the repository below :

- [RaspberryPi-AS3935 (Created by Phil Fenstermacher)](https://github.com/pcfens/RaspberryPi-AS3935/wiki/Calibration-Sample)

From the datasheet of AS39395 :
>The AS3935 uses a loop antenna based on parallel LC resonator. The antenna has to be designed to have its resonance frequency at 500kHz and a quality factor of around 15.
> ...
> It is necessary to tune the antenna with an accuracy of ±3.5% to optimize the performance of the signal validation and distance estimation.

For a better performance of the AS3935, you need to use this program and an oscilloscope (or any devices that can measure the frequency up to 40kHz) to measure the signal output from IRQ can find the number which matches 31.25kHz best.

__(We use the default value of the register REG0x03[7:6] which is 00 to set the division ratio to 16, so the best frequency should around 500/16=31.25kHz)__

### 3. [RPi_AS3935.py](./RPi_AS3935.py)
A basic class used for interacting with the AS3935 lightning sensor from a Raspberry Pi over I2C.
- [Original RPi_AS3935.py (pypi)](https://pypi.org/project/RPi_AS3935/)

The code for adjusting `WDTH` and `SREJ` outside in this program is below : 
```
def set_WDTH(self, WDTH):
    self.read_data()

    write_WDTH = (self.registers[0x01] & 0xF8) + WDTH
    self.set_byte(0x01, write_WDTH)

def set_SREJ(self, SREJ):
    self.read_data()

    write_SREJ = (self.registers[0x02] & 0xF8) + SREJ
    self.set_byte(0x02, write_SREJ)
```

### 4. [AS3935_DataVerMan.py](./AS3935_DataVerMan.py)
As the `AS3935.py` uses a watchdog when detecting lightning, it's not easy to let the program save the data matrix periodically for backup multiple versions. So I write 


## Atmosphere Sensor Module
### 1. [BME280.py](./BME280.py)
### 2. [RPi_BME280.py](./RPi_BME280.py)

## System Condition Module ([Condition.py](./Condition.py))

## Synchronize With Google Cloud ([Sync.py](./Sync.py))

## Shell Scripts
### 1. [run.sh](./run.sh)
- Scirpt for running all modules in several seperate tmux sessions.

- A `git pull origin main` on the head is for getting the latest version of scirpts before running.

- Use `echo` before python command in `bme280` and `condition` sessions for prevent some unexpected close of sessions caused by the sensor of BME280.

- You can let this script run at the startup. However, be attention that as `Sync.py` run the sychronization process immediately after the startup, you need to wait for the connection of network. Here is a sample by using `systemd` to run `run.sh` after the connection established when boot up. 
    1. Create a service called `RunLLS`
    ```
    $ sudo nano  /lib/systemd/system/RunLLS.service
    ```
    2. Add the following text, use `network-online.target` for running the script after network established
       
       __(The file `RunLLS.service` can be found in the folder `SetStartupRunning`, you can copy it to `~/lib/systemd/system/`)__
    ```
    [Unit]
    Description=My Script Service
    Wants=network-online.target
    After=network-online.target
    
    [Service]
    Type=simple
    User=pi
    ExecStart=/bin/sh /home/pi/Lightning_Location_System/run.sh
    RemainAfterExit=true

    [Install]
    WantedBy=multi-user.target
    ```
   3. Set priorities
    ```
    $ sudo chmod 744 /home/pi/Lightning_Location_System/run.sh
    $ sudo chmod 664 /lib/systemd/system/RunLLS.service
    $ sudo systemctl daemon-reload
    ```
   4. Enable services
    ```
    $ sudo systemctl enable systemd-networkd
    $ sudo systemctl enable RunLLS.service
    ```
   5. Reboot to test
    ```
    $ sudo reboot
    ```
  __You can use `SetStartupRunning.sh` in the folder `SetStartupRunning` to run the commands from step 3 to 5__

### 2. [kill.sh](./kill.sh)
Script for killing all tmux sessions.
You can specify the sessions you want to kill in this script.

### 3. [DeleteData.sh](./DeleteData.sh)
Script for deleting all data in the local folders when debug program.

You should confirm your action before the deletion. (Input `Y` to confirm)

__<span style="color: red; ">But be attention!!! This is very dangerous when you have old data on the cloud especially when `Sync.py` is running. </span>__

__<span style="color: red; ">I highly recommend you to check the data on the cloud and backup the data whether it's really useful before the deletion. </span>__


![SunShield](./images/System_LightningSensor.png?raw=true "sunshield")
![PlasticBox](./images/System_PlasticBox.png?raw=true "plasticbox")
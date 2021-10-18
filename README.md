# LightningLocationSystem

![SunShield](/images/System_LightningSensor.png?raw=true "sunshield")
![PlasticBox](/images/System_PlasticBox.png?raw=true "plasticbox")


## CommonParameters.py


## Lightning Sensor Module
### 1. AS3935.py
### 2. AS3935_Calibration.py
### 3. AS3935_DataVerMan.py
### 4. RPi_AS3935.py

## Atmosphere Sensor Module
### 1. BME280.py
### 2. RPi_BME280.py

## System Condition Module (Condition.py)

## Synchronize With Google Cloud (Sync.py)

## Shell Scripts for Raspberry Pi
### 1. run.sh
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

### 2. kill.sh
Script for killing all tmux sessions.
You can specify the sessions you want to kill in this script.


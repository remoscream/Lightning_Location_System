# LightningLocationSystem

![Alt text](/images/System_LightningSensor.png?raw=true "Optional Title")


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
    ```
    [Unit]
    Description=My Script Service
    Wants=network-online.target
    After=network-online.target
    
    [Service]
    Type=simple
    User=pi
    WorkingDirectory=/home/pi
    ExecStart=/home/pi/Lightning_Location_System/run.sh
    
    [Install]
    WantedBy=multi-user.target
    ```
   3. Enable services
    ```
    $ sudo systemctl enable systemd-networkd
    $ sudo systemctl enable RunLLS.service
    ```
  4. Test function and reboot
    ```
    $ sudo systemctl start RunLLS.service
    $ sudo reboot
    ```

### 2. kill.sh
Scirpt for killing all tmux sessions.
You can specify the sessions you want to kill in this script.


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


### 2. kill.sh
Scirpt for killing all tmux sessions.
You can specify the sessions you want to kill in this script.


# LightningLocationSystem

## 1. BME280
Main program for running BME280 weather sensor.


## 2. AS3935
Main program for running AS3935 lightning sensor.

## 3. RPi_AS3935
A basic class used for interacting with the AS3935 lightning sensor from a Raspberry Pi over I2C.

## 4. VerMan_AS3935
Managing the version of data.

## 5. Condition
Monitoring temperature and humidity of the box which Raspberry Pi and other equipments inside. Also, change the speed of ventilator if necessary.

The part of BME280 initialization skipped the pressuring measurement (osrs_p = 0).
As no pressure measured, the definition of rows in `dataset()` is different from 'BME280.py'.

The rows' definition of `dataset()` in this script shows below :

|  |  |  |  |  |  |  |  |  |  |  |  |  |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Row Number | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
| Defination | Year | Month | Day | Hour | Minute | Second | Box Temperature ('C) | Box Humidty (%) | CPU Temperature ('C) | CPU Frequency (GHz) | CPU Load (%) | Memory Used (M) |

## 6. Sync
Synchronize data in USB stick to google drive.


import os
import time
import subprocess
import CommonParameters as cp

# Find hostname
gdrive_foldername = '%s' % os.uname()[1]    # The folder name in cloud should be same as hostname of raspi

# Set file address of data in cloud
CloudFileAddress_as3935 = gdrive_foldername + '/data_as3935'
CloudFileAddress_bme280 = gdrive_foldername + '/data_bme280'
CloudFileAddress_condition = gdrive_foldername + '/data_condition'

if __name__ == '__main__':
    try:
        while True:
            # Use rclone to synchronize with google cloud
            subprocess.run('rclone sync ' + cp.FileAddress_as3935 + ' gdrive:' + CloudFileAddress_as3935, shell=True,
                           encoding='utf-8', stdout=subprocess.PIPE)
            subprocess.run('rclone sync ' + cp.FileAddress_bme280 + ' gdrive:' + CloudFileAddress_bme280, shell=True,
                           encoding='utf-8', stdout=subprocess.PIPE)
            subprocess.run('rclone sync ' + cp.FileAddress_condition + ' gdrive:' + CloudFileAddress_condition,
                           shell=True, encoding='utf-8', stdout=subprocess.PIPE)

            time.sleep(cp.TimeStep/2)   # Synchronize data to cloud by half the period of local

    except KeyboardInterrupt:
        print('\033[0J\n' + 'Process broken by user...')
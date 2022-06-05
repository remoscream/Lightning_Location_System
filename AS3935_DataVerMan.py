import functions_common as fun
import CommonParameters as cp
import time
import shutil

if __name__ == '__main__':
    try:
        # Initialization
        filename_old = 'data_as3935.csv'

        time.sleep(20)  # wait for AS3935.py create first file
        while True:
            _, time_text = fun.get_time_now()
            filename_new = 'data_as3935_' + time_text + '.csv'

            # Backup data
            shutil.copy(cp.FileAddress_as3935 + filename_old, cp.FileAddress_as3935 + filename_new)

            # Waiting for next period
            time.sleep(cp.SyncPeriod)

    except KeyboardInterrupt:
        print('\033[0J\n' + 'Synchronize process broken by user...')

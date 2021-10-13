import CommonParameters as cp
import time
import shutil
from datetime import datetime


# Get time text (now)
def get_time_text():
    dt_now = datetime.now()
    time_now_text = dt_now.strftime("%m-%d-%H-%M-%S")

    return time_now_text


if __name__ == '__main__':
    try:
        # Initialization
        filename_old = 'data_as3935.csv'

        time.sleep(20)  # wait for AS3935.py create first file
        while True:
            time_text = get_time_text()
            filename_new = 'data_as3935_' + time_text + '.csv'

            # Backup data
            shutil.copy(cp.FileAddress_as3935 + filename_old, cp.FileAddress_as3935 + filename_new)

            # Waiting for next period
            time.sleep(cp.SyncPeriod)

    except KeyboardInterrupt:
        print('\033[0J\n' + 'Synchronize process broken by user...')

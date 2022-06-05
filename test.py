import functions_common as fun
import time

dateset = []

for i in range(0, 5, 1):
    currentdata = [0, 0]
    dt_now_reformat_str, _ = fun.get_time_now()

    currentdata[0] = dt_now_reformat_str
    currentdata[1] = i

    dateset.append(currentdata)

    time.sleep(1)

print(dateset)

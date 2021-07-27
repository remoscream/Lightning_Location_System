import numpy as np
import datetime


def get_time():
    time_now_int = np.zeros((1, 6))

    dt_now = datetime.datetime.now()
    time_now_text_terminal = dt_now.strftime("%m/%d %H:%M:%S")
    time_now_text_file = dt_now.strftime("%m-%d-%H-%M-%S")

    time_now_int[0, 0] = float(dt_now.strftime("%Y"))
    time_now_int[0, 1] = float(dt_now.strftime("%m"))
    time_now_int[0, 2] = float(dt_now.strftime("%d"))
    time_now_int[0, 3] = float(dt_now.strftime("%H"))
    time_now_int[0, 4] = float(dt_now.strftime("%M"))
    time_now_int[0, 5] = float(dt_now.strftime("%S"))

    return time_now_text_terminal, time_now_text_file, time_now_int

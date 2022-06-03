import csv
from datetime import datetime


def save_list_to_csv(filepath, data, header):
    with open(filepath, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def get_time_now():
    dt_now = datetime.now()
    dt_now_reformat_str = dt_now.strftime("%Y/%m/%d %H:%M:%S")
    dt_now_reformat_int = dt_now.strftime("%Y%m%d%H%M%S")

    return dt_now_reformat_str, dt_now_reformat_int

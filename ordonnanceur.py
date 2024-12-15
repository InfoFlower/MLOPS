import get_data
from make_csv import csv_maker
import time
while True:
    api_calleur=get_data.get_data()
    api_calleur()
    csv_maker()
    predict_model
    time.sleep(60)
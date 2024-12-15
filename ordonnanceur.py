import get_data
import time
while True:
    api_calleur=get_data.get_data()
    api_calleur()
    time.sleep(300)
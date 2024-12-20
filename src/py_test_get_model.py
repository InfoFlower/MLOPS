from mlflow.client import MlflowClient
from data_processing import make_great_dataset,make_future
import mlflow.pyfunc
import pandas as pd
df=pd.read_csv('data/station_detail_temp.csv')
to_fit=['last_reported', 'DAY', 'DAY OF WEEK','DAY OF YEAR', 'HOUR', 'MIN', 'numDocks']
col_to_drop=['MONTH','YEAR','stationCode','is_installed','station_id','is_returning','is_renting','num_bikes_available','num_docks_available','numDocksAvailable']
key=['last_reported','HOUR','numBikesAvailable']
col_sum_1='numBikesAvailable'
col_sum_2='numDocksAvailable'
col_make_sum='numDocks'
col_make_date='last_reported'
test=make_great_dataset(col_to_drop,key)
df=test('data/station_detail_temp.csv',col_sum_1,col_sum_2,col_make_sum,col_make_date=col_make_date)



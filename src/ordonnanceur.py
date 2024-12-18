
from data_collecting import csv_maker,get_data,make_data_set
from data_processing import make_great_dataset
from data_modelisation import model_maker_tester


import time
import logging 
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)

col_to_drop=['MONTH','YEAR','stationCode','is_installed','station_id','is_returning','is_renting','num_bikes_available','num_docks_available','numDocksAvailable']
key=['last_reported','HOUR','numBikesAvailable']

col_sum_1='numBikesAvailable'
col_sum_2='numDocksAvailable'
col_make_delta = 'numBikesAvailable'
col_make_sum='numDocks'
col_make_date='last_reported'

file_path='../data/init_data.csv'
target=''
to_fit=['last_reported', 'DAY', 'DAY OF WEEK','DAY OF YEAR', 'HOUR', 'MIN', 'numDocks']
to_pred='numBikesAvailable'
cat_cols=None

model_maker_tester_api=model_maker_tester(cat_cols,to_fit,to_pred)
df=make_data_set(file_path)

api_calleur=get_data()
while True:
    api_calleur()
    csv_maker(input_dir = './data/RAW/',data_in_file='data/station_detail_temp.csv',output_csv_file='data/station_detail_temp.csv',is_in=True,delete=True)
    df=pd.read_csv('./data/raw/station_detail_temp.csv')
    #make predict data_set (futur) ==> package data_processing
    data_to_pred=df[to_fit]
    logging.info(f'PREDICTION FOR ===== {prediction}')
    #make viz of predict ==> package data_visualisation 
    if int(time.strftime('%H%M')) in  (1200,0000):
        #get train test data ==> package models
        collected_data=get_train_data()
        challenger_model=train_model(champion_model,collected_data)
        #faire process de valuation de models with new model and old one (type of model & hyperparam (grid_search_cv)) ==> package models
        which_model=test_models(new_model=challenger_model,OG_model=champion_model,data_test=f'./data/station_detail_temp.csv')
    time.sleep(59)
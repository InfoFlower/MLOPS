from data_processing import csv_maker,get_data,make_data_set
from models import model_maker_tester
import time
import logging
import pandas as pd

file_path='../data/init_data.csv'
target=''
to_fit=['feature1','feature2','feature3']
cat_cols=None

model_maker_tester_api=model_maker_tester()
df=make_data_set(file_path)


challenger_model=model_maker_tester(model,'logistic',df,flg_first=True)
champion_model=''
while True:
    api_calleur=get_data()
    api_calleur()
    csv_maker(input_dir = './data/RAW/',data_in_file='data/station_detail_temp.csv',output_csv_file='data/station_detail_temp.csv',is_in=True,delete=True)
    prediction=predict_model(challenger_model,'station_detail_temp.csv')
    prediction_moment = f'{time.strftime("%D|%H")}:{int(time.strftime("%M"))+1}'
    logging.info(f'PREDICTION FOR {prediction_moment} ===== {prediction}')
    if int(time.strftime('%H%M')) in  (1200,2400):
        collected_data=get_train_data()
        challenger_model=train_model(champion_model,collected_data)
        which_model=test_models(new_model=challenger_model,OG_model=champion_model,data_test=f'./data/station_detail_temp.csv')
    time.sleep(59)
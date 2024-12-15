from data_processing import csv_maker,get_data,get_train_data
from models import predict_model,train_model,test_models
import time
import logging


challenger_model=''
champion_model=''
while True:
    api_calleur=get_data()
    api_calleur()
    csv_maker()
    prediction=predict_model(challenger_model,'station_detail_temp.csv')
    prediction_moment = f'{time.strftime("%d|%H")}:{int(time.strftime("%M"))+1}'
    logging.info(f'PREDICTION FOR {prediction_moment} ===== {prediction}')
    if int(time.strftime('%H%M')) in  (1200,2400):
        csv_maker(input_dir='./data/old_daily/',
                  output_dir='./data/used/',
                  output_csv_file=f'./data/data_test-{ time.strftime("%y_%m_%d") }.csv')
        collected_data=get_train_data()
        challenger_model=train_model(champion_model,collected_data)
        which_model=test_models(new_model=challenger_model
                                ,OG_model=champion_model
                                ,data_test=f'./data/data_test-{ time.strftime("%y_%m_%d") }.csv')
    time.sleep(60)
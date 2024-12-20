
from src.data_collecting import csv_maker,get_data
from src.data_processing import make_great_dataset,make_future
from src.data_modelisation import model_maker_tester
import os
import mlflow.pyfunc
from mlflow.client import MlflowClient
import time
import logging 
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)


####################################  MLFLOW CONF  ####################################

client = MlflowClient(tracking_uri="file:mlruns")
experiment_name = "Velib"
experiment = client.get_experiment_by_name(experiment_name)

########################################################################################


#############################  MODEL MAKER TESTER CONF  #################################

cat_cols=None
to_fit=['last_reported', 'DAY', 'DAY OF WEEK','DAY OF YEAR', 'HOUR', 'MIN', 'numDocks']
to_pred='numBikesAvailable'

param_grid = {
    'n_estimators': [50, 100, 200],  
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth': [None, 5, 10],  
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 5, 10],
    'bootstrap': [True, False]  
}

model_maker_tester_api=model_maker_tester(cat_cols,to_fit,to_pred)

########################################################################################


#################################  MAKE GREAT DATASET CONF  #################################
col_to_drop=['MONTH','YEAR','stationCode','is_installed','station_id',
             'is_returning','is_renting','num_bikes_available','num_docks_available','numDocksAvailable']
key=['last_reported','HOUR','numBikesAvailable']

make_great_dataset_api=make_great_dataset(col_to_drop,key)

#################################  DATA PROCESSING CONF  #####################################

col_sum_1='numBikesAvailable'
col_sum_2='numDocksAvailable'
col_make_delta = 'numBikesAvailable'
col_make_sum='numDocks'
col_make_date='last_reported'

########################################################################################


api_calleur=get_data()
while True:
    flag_drop_file=False
    api_calleur()
    csv_maker(input_dir = './data/RAW/',data_in_file='data/station_detail_live.csv',output_csv_file='data/station_detail_live.csv',is_in=True,delete=True)    
    if int(time.strftime('%H%M')) == int(time.strftime('%H%M')):#'2359':
        try:
            #data loading and processing
            df=make_great_dataset_api('./data/station_detail_live.csv',col_sum_1,col_sum_2,col_make_sum,col_make_date=col_make_date)
            df.to_csv(f'./data/df_{time.strftime("%y%m%d")}.csv')
            last_csv=f'./data/df_{time.strftime("%y%m%d")}.csv'
            if flag_drop_file : os.remove(last_csv)
            #get last model mlflow
            latest_run = client.search_runs(experiment_ids=[experiment.experiment_id], order_by=["start_time DESC"], max_results=1)[0]
            model_uri = f"runs:/{latest_run.info.run_id}/RandmForest/"
            logging.info(f'MODEL URI ====== {model_uri}')
            champion_model = mlflow.sklearn.load_model(model_uri)
            logging.info(f'MODEL URI ====== {champion_model}')
            #train model
            new_champion,score_new_model=model_maker_tester_api(champion_model,'RandmForest',df,f'V0.0.1{time.strftime("%y%m%d")}',param_grid)
            logging.info(f'NEW MODEL SCORE ====== {score_new_model}')
            flag_drop_file=True
        except Exception as e:
            logging.error(f'ERROR ===== {e}')
            with open('./data/error.log','w') as f:
                f.write(f'{time.strftime("%y%m%d%H%M%S")} : {e} \n')
    try:
        #prediction
        prediction=new_champion.predict(make_future(df,'HOUR',to_fit))
        logging.info(f'PREDICTION FOR ===== {prediction}')
    except Exception as e:
        logging.error(f'ERROR ===== {e}')
    time.sleep(59)

from data_processing import make_great_dataset,make_future
from data_modelisation import model_maker_tester
import os
from sklearn.ensemble import RandomForestClassifier
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
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
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
champion_model=RandomForestClassifier()
########################################################################################
flag_drop_file=False
#data loading and processing



df=make_great_dataset_api('__init__/init_data.csv',col_sum_1,col_sum_2,col_make_sum,col_make_date=col_make_date)
df.to_csv(f'data/df_{time.strftime("%y%m%d")}.csv')
last_csv=f'data/df_{time.strftime("%y%m%d")}.csv'
if flag_drop_file : os.remove(last_csv)
#get last model mlflow
#train model
new_champion,score_new_model=model_maker_tester_api(champion_model,'RandmForest',df,f'V0.0.1{time.strftime("%y%m%d")}',param_grid,flg_first=True)
logging.info(f'NEW MODEL SCORE ====== {score_new_model}')
#prediction
prediction=new_champion.predict(make_future(df,'HOUR',to_fit))
logging.info(f'PREDICTION FOR ===== {prediction}')
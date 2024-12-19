import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from data_modelisation import model_maker_tester
from data_processing import make_great_dataset

param_grid = { 
    'n_estimators': [200, 500],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [4,5,6,7,8],
    'criterion' :['gini', 'entropy']
}

#Var d'initialisation du data_processing
col_to_drop=['MONTH','YEAR','stationCode','is_installed','station_id','is_returning','is_renting','num_bikes_available','num_docks_available','numDocksAvailable']
key=['last_reported','HOUR','numBikesAvailable']
#Var pour l'appel (traitements à faire)
col_sum_1='numBikesAvailable'
col_sum_2='numDocksAvailable'
col_make_delta = 'numBikesAvailable'
col_make_sum='numDocks'
col_make_date='last_reported'
test=make_great_dataset(col_to_drop,key)
df=test('data/station_detail_temp.csv',col_sum_1,col_sum_2,col_make_sum,col_make_date=col_make_date)
to_fit=['last_reported', 'DAY', 'DAY OF WEEK','DAY OF YEAR', 'HOUR', 'MIN', 'numDocks']
to_pred='numBikesAvailable'
cat_cols=None
model_maker = model_maker_tester(cat_cols,to_fit,to_pred)
model_maker(RandomForestClassifier(random_state=42),'LogisticRegression',df,'V0_test_ipynb',param_grid,'Velib',flg_first=True)
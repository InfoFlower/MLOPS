from data_modelisation import model_maker_tester
from data_processing import make_great_dataset
from data_processing import make_future
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier

haha="""
param_grid = {
    'copy_X' :[True,False], 
    'fit_intercept':[True,False],
    'positive':[True,False]
}
"""_
param_grid = {
    'n_estimators': [50, 100, 200],  # number of trees in the forest
    'max_features': ['auto', 'sqrt', 'log2'],  # maximum number of features to consider at each split
    'max_depth': [None, 5, 10],  # maximum depth of the tree
    'min_samples_split': [2, 5, 10],  # minimum number of samples required to split an internal node
    'min_samples_leaf': [1, 5, 10],  # minimum number of samples required to be at a leaf node
    'bootstrap': [True, False]  # whether to use bootstrap sampling when building trees
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
model=RandomForestClassifier()
model_fitted=model_maker(model,'Linear_reg',df,'V0_py_test',param_grid,'Velib',flg_first=True)
print(model_fitted.predict(make_future(df,'MIN',to_fit)))
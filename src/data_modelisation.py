from sklearn import metrics
import logging
import mlflow as mf
from sklearn.model_selection import train_test_split
mf.sklearn.autolog()
logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)
from mlflow.models import infer_signature
from sklearn.model_selection import GridSearchCV
from mlflow.data.pandas_dataset import PandasDataset

mf.set_tracking_uri("file:mlruns")

def log_model_version(model,model_name,signature,data,scores,hyperparam_value,exprience_name,version):
    """
    """
    mf.set_experiment(experiment_name=exprience_name)
    data.to_csv('temp/train_data.csv')
    data_file_path='temp/train_data.csv'
    mf.log_param("version", version)
    with mf.start_run(nested=True) as run:
        mf.sklearn.log_model(model,model_name,signature= signature)
        for metric_name, metric_value in scores.items():
            mf.log_metric(metric_name, metric_value)
        for param_name, param_value in hyperparam_value.items():
            mf.log_param(param_name, param_value)
        logging.info(f"Model logged with run_id: {run.info.run_id}")

class model_maker_tester:
    def __init__(self,cat_cols,fit_cols,y_col):
        self.cat_cols=cat_cols
        self.fit_cols=fit_cols
        self.y_col=y_col

    def score(self,model,X_test,y_test):
        """
        Affichage des metrics
        """
        return {'accuracy' :        round(float(metrics.precision_score(y_test,model.predict(X_test),average='macro')),2)}


    def make_dummies_X_y(self,data,flg_train_test,test_size=0.33,rnd_state=42):
        if self.cat_cols is not None : Xy=data.to_dummies(columns=self.cat_cols,drop_first=False)
        else : Xy=data
        logging.debug(f'Jeu de donnee : {Xy}')
        X=Xy[self.fit_cols]
        y=data[self.y_col]
        logging.info('CREATION TRAIN TEST DATASETS')
        if flg_train_test : ret=train_test_split(X,y,test_size=test_size,random_state=rnd_state)
        else : ret = X,y
        return ret
    
    def __call__(self,model,model_name,data,version,param_grid,experience_name='Velib',flg_to_score=True,flg_first=False):
        logging.debug(f'DATA : {data}')
        model=model
        model_name=model_name
        X_train, X_test, y_train, y_test = self.make_dummies_X_y(data,flg_train_test=True)
        X,y=self.make_dummies_X_y(data=data,flg_train_test=False)
        logging.info(f'Data to fit or predict : {X,y,X_train,X_test,y_train,y_test}')
        if flg_to_score :
            logging.info('FITTING DATA')
            if flg_first:
                grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy',n_jobs=-1)
                grid_search.fit(X_train, y_train)
                params = grid_search.best_params_
                model = grid_search.best_estimator_
            logging.info('START SCORING')
            score=self.score(model,X_test,y_test)
            logging.info(f'SCORE DU MODELE  {score}')
            signature=infer_signature(X,model.predict(X))
            log_model_version(model,model_name,signature,data,score,model.get_params(),experience_name,version)
        #prevoir un return (soit score soit model)
        else :
            logging.debug(f'DATA TO PREDICT {X}')
            logging.info(f'PREDICTION DU MODEL {model.predict(X)}')
        return model
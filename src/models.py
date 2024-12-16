from sklearn import metrics
import logging
import mlflow as mf
from sklearn.model_selection import train_test_split
mf.set_tracking_uri('http://172.0.0.1:8080')
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)

def log_model_version(model,model_name,data,scores,hyperparam_value):
    """
    """
    data.write_csv('temp/train_data.csv')
    data_file_path='temp/train_data.csv'
    with mf.start_run() as run:
        mf.sklearn.log_model(model,model_name)
        for metric_name, metric_value in scores.items():
            mf.log_metric(metric_name, metric_value)
        mf.log_artifact(data_file_path)
        mf.log_param("hyperparam_name", hyperparam_value)
        run_id = run.info.run_id
        logging.info(f"Model logged with run_id: {run_id}")

class model_maker_tester:
    def __init__(self,cat_cols,fit_cols,y_col):
        self.cat_cols=cat_cols
        self.fit_cols=fit_cols
        self.y_col=y_col

    def score(self,X_test,y_test):
        """
        Affichage des metrics
        """
        return {'accuracy' :        round(float(metrics.precision_score(y_test,self.model.predict(X_test))),2),
                       'auc' :      round(float(metrics.roc_auc_score(y_test,self.model.predict(X_test))),2),
                       'Gauc' :      round(float(metrics.roc_auc_score(y_test,self.model.predict_proba(X_test)[:,1], average='weighted')),2),
                       'f1-score' : round(float(metrics.f1_score(y_test,self.model.predict(X_test))),2)}


    def make_dummies_X_y(self,data,flg_train_test,test_size=0.33,rnd_state=42):
        if self.cat_cols is not None : Xy=data.to_dummies(columns=self.cat_cols,drop_first=False)
        else : Xy=data
        X=Xy[self.fit_cols]
        y=data[self.y_col]
        logging.info('CREATION TRAIN TEST DATASETS')
        if flg_train_test : ret=train_test_split(X,y,test_size=test_size,random_state=rnd_state)
        else : ret = X,y
        return ret
    
    def __call__(self,model,model_name,data,flg_to_score=True,flg_first=False):
        logging.debug(f'DATA : {data}')
        self.model=model
        self.model_name=model_name

        if flg_to_score :
            X_train, X_test, y_train, y_test = self.make_dummies_X_y(data,flg_train_test=True)
            logging.info('FITTING DATA')
            if flg_first: self.model.fit(X_train,y_train)
            logging.info('START SCORING')
            score=self.score(X_test,y_test)
            ret=score
            logging.info(f'SCORE DU MODELE  {score}')
            log_model_version(model,model_name,data,score,model.get_params())

        else :
            X,y=self.make_dummies_X_y(data=data,flg_train_test=False)
            logging.debug(f'DATA TO PREDICT {X}')
            logging.info(f'PREDICTION DU MODEL {self.model.predict(X)}')
        
import polars as pl
import sklearn as sk
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression



def predict_model(model,data):
    return model.predict(data)
    

def train_model(model,data):
    return model.fit(data)

def test_models(data_test
                ,new_model
                ,OG_model):
    results='champion'
    score_challenger = scoring(new_model,data_test)
    score_champion = scoring(OG_model,data_test)
    if score_challenger>score_champion : 
        results='challenger'
    return results
    

def score(X_train,X_test,y_train,y_test,model):
    """
    Affichage des metrics
    """
    return {'accuracy' :        round(float(metrics.precision_score(y_test,model.predict(X_test))),2),
                   'auc' :      round(float(metrics.roc_auc_score(y_test,model.predict(X_test))),2),
                   'Gauc' :      round(float(metrics.roc_auc_score(y_test,model.predict_proba(X_test)[:,1], average='weighted')),2),
                   'f1-score' : round(float(metrics.f1_score(y_test,model.predict(X_test))),2)}

def score_cv(X_train,X_test,y_train,y_test,trained_model):
    return {'best params': trained_model.best_params_,
            'associed f1-score': score(X_train,X_test,y_train,y_test,trained_model)}


def all_calc(df,
             model,
             cols,
             top_cv=False,
             test_size=0.33,
             rnd_state=11,
             new_data=None,
             plot=False):
    """
    Segmente le jeu de données en train test size si besoin
    puis peut faire les predictions ou les scores dépendamment du besoin
    """
    df=pd.get_dummies(df,columns=cols)
    X=df[df.columns[:-2]]
    y=df['income_>50K']
    if new_data is None:
        logging.info('CREATION TRAIN TEST DATASETS')
        X_train, X_test, y_train, y_test =train_test_split(X,y,test_size=test_size,random_state=rnd_state)
    else:
        X_train,y_train=(X,y)
    ret={}
    logging.info('FITTING DATA')
    model.fit(X_train,y_train)
    if new_data is None:
        logging.info('START SCORING')
        if top_cv==True:
            ret[i[1]]=score_cv(X_train,X_test,y_train,y_test,i[0])
        else:
            ret[i[1]]=score(X_train,X_test,y_train,y_test,i[0])
    if new_data is not None:
        ret[i[1]]=[i[0].predict(pl.get_dummies(new_data,columns=cols[:-1])),i[1]]
    return ret
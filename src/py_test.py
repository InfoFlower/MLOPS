import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import logging
from data_modelisation import model_maker_tester
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)

####### JEU DE DONNEES TEST FAIT PAR IA #############
# Créer des données de test
data = {
    "feature1": np.random.rand(100),
    "feature2": np.random.rand(100),
    "feature3": np.random.rand(100),
    "target": np.random.randint(0, 2, 100)  # Target binaire pour un exemple de classification
}

# Créer un DataFrame Polars
df = pd.DataFrame(data)
model = LogisticRegression()


test=model_maker_tester(None,['feature1','feature2','feature3'],'target')
know=test(model,'logistic',df,'V0.1',flg_first=True)
print(know)
model_test=know
data_to_pred=df[['feature1','feature2','feature3']]
print('PREDICTION ',test(model_test,'logistic',df,flg_to_score=False))
print('SCORING ',test(model_test,'logistic',df))
print(model_test.get_params())

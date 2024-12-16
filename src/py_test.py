import numpy as np
import polars as pl
from sklearn.linear_model import LogisticRegression
from models import model_maker_tester

####### JEU DE DONNEES TEST FAIT PAR IA #############
# Créer des données de test
data = {
    "feature1": np.random.rand(100),
    "feature2": np.random.rand(100),
    "feature3": np.random.rand(100),
    "target": np.random.randint(0, 2, 100)  # Target binaire pour un exemple de classification
}

# Créer un DataFrame Polars
df = pl.DataFrame(data)
model = LogisticRegression()


test=model_maker_tester(None,['feature1','feature2','feature3'],'target')
know=test(model,'logistic',df,flg_first=True)
model_test=know[1][0]
data_to_pred=df[['feature1','feature2','feature3']]
print('PREDICTION ',test(model_test,'logistic',df,flg_to_score=False))
print('SCORING ',test(model_test,'logistic',df))
print(model_test.get_params())

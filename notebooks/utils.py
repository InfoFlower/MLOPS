import pandas as pd
import os


def extract(df=None,num_rest=1,deb=0,fin=999):
    for i in range(deb,fin):
        path ="../data/restaurant_+" str(num_rest) +"_week_" + str(i).zfill(3) + ".csv"
        if os.path.isfile(path):
            if df is None:
                df=pd.read_csv(path)
                df['Week']=i
            else:
                df_=pd.read_csv(path)
                df_['Week']=i
                df = pd.concat([df,df_])
    return df.reset_index()
import pandas as pd
import datetime

class make_great_dataset:
    def __init__(self,col_to_drop,key):
        self.col_to_drop=col_to_drop
        self.key=key

    def __call__(self,file_path,col_sum_1,col_sum_2,col_make_sum,col_make_delta=None,col_make_date=None):
        data=pd.read_csv(file_path)
        if col_make_sum is not None : data[col_make_sum]=data[col_sum_1]+data[col_sum_2]
        data_clean=data.drop(self.col_to_drop,axis=1)
        if col_make_date is not None : data_clean[col_make_date] = self.make_date(data,col_make_date)
        data_clean_unique=data_clean.drop_duplicates(self.key)
        data_featured=data_clean_unique.reset_index(drop=True)[1:]
        if col_make_delta is not None :  data_featured['delta']=self.delta(data_clean_unique.reset_index(),col_make_delta)
        return data_featured
    
    def delta(self,data,col):
        """
        THIS FUNCTION NEED TO BE FITTED IN A SUBSET WITH THE FIRST ROW DELETED
        """
        data_n=list(data[col][1:])
        data_n_1=(data[col][:-1])
        data_delta=[]
        for i in range(len(data_n)):
            data_delta.append(data_n[i]-data_n_1[i])
        return data_delta

    def make_sum(self,data):
        return data[self.col_1]+data[self.col_2]

    def make_date(data,col):
        return [datetime.datetime.fromtimestamp(i).strftime('%Y%m%d') for i in data[col]]

    def from_data_to_delta_data(data):
        return data.reset_index(drop=True)[1:]
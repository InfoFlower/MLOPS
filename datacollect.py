import logging
import requests
import os
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
api_key = 'demo'

class get_api:
    def __init__(self,api_key : str, dtype:str,function:str='TIME_SERIES_DAILY'):
        self.api_key=api_key
        self.data_type=dtype
        self.function=function

    def __make_url(self,symbol : str):
        logging.debug(f'MAKE URL START')
        url=f'https://www.alphavantage.co/query?function={self.function}&symbol={symbol}&datatype={self.data_type}&apikey={self.api_key}'
        logging.debug(f'API CALL URL : {url}')
        return url
        
    def __get_data(self,url:str):
        """
        Fonction
        """
        logging.debug('FUNCTION API CALL TO DATA START')
        data=requests.get(url).text
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.abspath(os.path.join(base_dir, '../../data/new.csv'))
        with open(file_path,'w') as f:
            f.write(data)
        logging.debug('FUNCTION API CALL TO DATA END')
    
    def __call__(self,tocken):
        self.__get_data(self.__make_url(tocken))
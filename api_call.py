import logging
import requests
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)

class get_api:
    def __init__(self,api_key : str, dtype:str,function:str='TIME_SERIES_INTRADAY',interval:str='5min'):
        self.api_key=api_key
        self.data_type=dtype
        self.function=function
        self.interval=interval

        
    def __get_data(self,tocken:str,date_from:str,date_to:str):
        """
        Fonction
        """
        url=f"https://api.marketstack.com/v1/eod?access_key={self.api_key}"
        querystring = {"symbols":tocken,"date_from":date_from, "date_to":date_to,'limit':1000}
        logging.info('FUNCTION API CALL TO DATA START')
        response = requests.get(url, params=querystring)
        return response
    
    def __call__(self,tocken,date_from,date_to):
        return self.__get_data(tocken,date_from,date_to)
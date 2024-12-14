import os
from dotenv import load_dotenv
import logging

load_dotenv()  # Load .env file

api_key = os.getenv('API_KEY')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

class get_api:
    def __init__(self,api_key,db_username,db_password,dtype):
        self.api_key=api_key
        self.db_user=db_username
        self.db_pwd=db_password
        self.data_type=dtype
    
    def get_data(self,url,symbol,function='TIME_SERIES_DAILY'):
        """
        Fonction
        """
        logging.debug('FUNCTION API CALL TO DATA START')
        url=f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&datatype={self.data_type}&apikey={self.api}'
        logging.debug(f'API CALL URL : {url}')
        with open('data/cache.csv') as f:
            f.write(requests.get(url).text)
        logging.debug('FUNCTION API CALL TO DATA END')
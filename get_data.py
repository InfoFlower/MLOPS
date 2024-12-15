import logging 
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)
import requests as rq
import time

URLS=[('https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/gbfs.json','gbfs'),
      ("https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json",'stat_inf'),
      ("https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/system_information.json",'sys_inf')]

class get_data:
    def __init__(self,urls=URLS):
        logging.info('START GET DATA')
        for url,name in urls:
            logging.info(f'CALLING {url}')
            data=rq.get(url)
            file_path=f'./data/.sys/{name}.json'
            file_load=open(file_path,'w')
            file_load.write(data.text)
            file_load.close()
        self.nb_iter=0

    def __call__(self,url="https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"):
        logging.info('START OF PROC GET DATA')
        self.nb_iter+=1
        name=f"station_status_{time.strftime('%Y_%m_%d-%H_%M')}"
        file_writer=open(f'data/RAW/{name}.json','w')
        logging.info(f'CALLING { url }')
        file_writer.write(rq.get(url).text)
        file_writer.close()
        logging.info(f'FICHIER CREE {name}')
        logging.info('END OF PROC GET DATA')
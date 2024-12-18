import requests as rq
import time

import polars as pl
import time
import json
import os


Schema={'station_id'           : pl.Int64, 
'num_bikes_available'  : pl.Int64, 
'numBikesAvailable'    : pl.Int64, 
'num_docks_available'  : pl.Int64, 
'numDocksAvailable'    : pl.Int64, 
'is_installed'         : pl.Int64, 
'is_returning'         : pl.Int64, 
'is_renting'           : pl.Int64, 
'last_reported'        : pl.Int64, 
'stationCode'          : pl.String, 
'YEAR'                 : pl.Int32, 
'MONTH'                : pl.Int32, 
'DAY'                  : pl.Int32, 
'DAY OF WEEK'          : pl.Int32, 
'DAY OF YEAR'          : pl.Int32, 
'HOUR'                 : pl.Int32, 
'MIN'                  : pl.Int32}

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


def csv_maker(input_dir = './data/RAW/'
              ,output_dir='./data/old_daily/'
              ,data_in_file='data/station_detail_temp.csv'
              ,output_csv_file='data/station_detail_temp.csv'
              ,is_in=False
              ,Schema=Schema
              ,delete=False):
    if is_in:data_raw=pl.read_csv(data_in_file,schema=Schema)
    else : data_raw = pl.DataFrame(schema=Schema)
    for fichier in os.listdir(input_dir):
        chemin_complet = os.path.join(input_dir, fichier)
        with open(chemin_complet, 'r') as f:
            data = json.load(f)
        temp_df = pl.DataFrame(data['data']['stations'])['station_id'==213688169]['last_reported' not in list(data_raw['last_reported'])]
        temp_df = temp_df.with_columns([
            pl.lit(int(time.strftime('%y'))).alias('YEAR'),
            pl.lit(int(time.strftime('%m'))).alias('MONTH'),
            pl.lit(int(time.strftime('%d'))).alias('DAY'),
            pl.lit(int(time.strftime('%u'))).alias('DAY OF WEEK'),
            pl.lit(int(time.strftime('%j'))).alias('DAY OF YEAR'),
            pl.lit(int(time.strftime('%H'))).alias('HOUR'),
            pl.lit(int(time.strftime('%M'))).alias('MIN')
        ])
        temp_df = temp_df.drop("num_bikes_available_types")
        logging.debug(temp_df.schema)
        data_raw = pl.concat([data_raw, temp_df], how="vertical")
        if delete:os.remove(f"{input_dir}{fichier}")
        else : os.rename(f"{input_dir}{fichier}",f"{output_dir}{fichier}")
    logging.debug(f'NOM DU FICHIER DE SORTIE {output_csv_file}')
    data_raw.write_csv(data_in_file)
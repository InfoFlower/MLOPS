import logging 
import api_call as dc
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)
import json
import requests as rq

def proc_get_data():
    logging.info('START GET DATA')
    url='https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/gbfs.json'
    logging.info(f'CALLING {url}')
    data=rq.get(url)
    file_path=f'data/.sys/gbfs.json'
    file_load=open(file_path,'w')
    file_load.write(data.text)
    file_load.close()
    json_file= open(r"data\.sys\gbfs.json", 'r') 
    available_data=json.load(json_file)
    json_file.close()
    for i in available_data['data']['en']['feeds']:
        if i['name'] in ('gbfs','system_information'):
            name=f"{i['name']}"
            file_writer=open(f'data/.sys/{name}.json','w')
        else : 
            name=f"{i['name']}_{available_data['lastUpdatedOther']}"
            file_writer=open(f'data/{name}.json','w')
        logging.info(f'CALLING { i["url"] }')
        file_writer.write(rq.get(i['url']).text)
        file_writer.close()
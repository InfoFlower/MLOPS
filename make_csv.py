import polars as pl
import time
import json
import os


Schema=[('station_id',          pl.Int64),
        ('num_bikes_available', pl.Int64),
        ('numBikesAvailable',   pl.Int64),
        ('num_docks_available', pl.Int64),
        ('numDocksAvailable',   pl.Int64),
        ('is_installed',        pl.Int64),
        ('is_returning',        pl.Int64),
        ('is_renting',          pl.Int64),
        ('last_reported',       pl.Int64),
        ('stationCode',         pl.String),
        ('YEAR',                pl.Int32),
        ('MONTH',               pl.Int32),
        ('DAY',                 pl.Int32),
        ('DAY OF WEEK',         pl.Int32),
        ('DAY OF YEAR',         pl.Int32),
        ('HOUR',                pl.Int32),
        ('MIN',                 pl.Int32)]

def csv_maker(repertoire = './data/RAW/',Schema=Schema):
    data_raw = pl.DataFrame(schema=Schema)
    for fichier in os.listdir(repertoire):
        chemin_complet = os.path.join(repertoire, fichier)
        with open(chemin_complet, 'r') as f:
            data = json.load(f)
        temp_df = pl.DataFrame(data['data']['stations'])
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
        data_raw = pl.concat([data_raw, temp_df], how="vertical")
        os.rename(f"./data/RAW/{fichier}",f"./data/old/{fichier}")
    data_raw.write_csv('./data/stations_detail_temp.csv')
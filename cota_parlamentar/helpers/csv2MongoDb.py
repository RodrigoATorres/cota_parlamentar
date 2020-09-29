from dotenv import load_dotenv
load_dotenv()

import os
import json
import pandas as pd

from pymongo import MongoClient


if __name__ == '__main__':
    client = MongoClient('mongodb://%s:%s@127.0.0.1/?authSource=admin' % (os.getenv("MONGO_INITDB_ROOT_USERNAME"), os.getenv("MONGO_INITDB_ROOT_PASSWORD")))
    db = client.cota_parlamentar

    df = pd.read_csv('./data/AnoAtual.csv')
    records = json.loads(df.T.to_json()).values()
    db.despesas.insert(records)

    df = pd.read_csv('./data/Secretarios.csv')
    records = json.loads(df.T.to_json()).values()
    db.secretarios.insert(records)
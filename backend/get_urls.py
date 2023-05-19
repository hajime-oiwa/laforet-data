import sqlalchemy
import pandas as pd
import numpy as np

def get_url_table():
    #データベースのレコード取得
    user = "root"
    password = "h3470obobby"
    host = "localhost"
    port = "3306"
    database = "sales_DB"
    url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

    engine = sqlalchemy.create_engine(url)
    sql_query = 'select year, month, url from urls order by year, month'

    result = pd.read_sql(sql=sql_query, con=engine)
    result = result.to_numpy().tolist()

    return result
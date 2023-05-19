import sqlalchemy
import pandas as pd
def get_available_period():
    user = "xxxx"
    password = "xxxx"
    host = "xxxx"
    port = "xxxx"
    database = "xxxx"
    url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

    engine = sqlalchemy.create_engine(url)
    sql_query = 'select * from urls order by year, month'

    result = pd.read_sql(sql=sql_query, con=engine)
    year_list = result["year"].to_list()
    month_list = result["month"].to_list()
    available_period = {"全期間" : ["全期間"]}
    for i in range(len(year_list)):
        if year_list[i] in available_period:
            available_period[year_list[i]].append(month_list[i])
        else:
            available_period[year_list[i]] = [month_list[i]]
            
    return available_period
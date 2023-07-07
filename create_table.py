import csv
import io

import pandas as pd
import psycopg2
import sqlalchemy

from constants import *


def psql_insert_copy(table, conn, keys, data_iter):
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = io.StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)
        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name
        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)

def create_postgres_table(sales_data, name='sales_data'):
    # user = 'postgres'
    # password = '12345678'
    # dbname = 'test_20230706'
    # address = 'localhost'
    conn = sqlalchemy.create_engine(f'postgresql://{user}:{password}@{address}:5432/{dbname}')

    with psycopg2.connect(host=address,
                                  port=5432,
                                  database=dbname,
                                  user=user,
                                  password=password
                                  ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS public;")

    sales_data.to_sql(name, conn, schema='public', method=psql_insert_copy, if_exists='replace')

if __name__ == '__main__':
    with open('../sales_data.csv', 'r') as f:
        sales_data = pd.read_csv(io.StringIO(f.read()))
    sales_data['EUROPE'] = sales_data['TERRITORY']=='EMEA'
    sales_data.columns = [c.lower() for c in sales_data.columns]
    create_postgres_table(sales_data)
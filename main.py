import io

import duckdb
import environ
import pandas as pd
import sqlalchemy
import streamlit as st
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

from constants import *
#from create_table import create_postgres_table
from unit_tests import test_queries

environ.Env.read_env()


class NaturalQuery:
    def __init__(self, data_columns,
                 llm=OpenAI(model_name='gpt-3.5-turbo-16k', openai_api_key=environ.Env()('OPENAI_API_KEY'))):
        self.data_columns = data_columns
        self.llm = llm
        db = SQLDatabase.from_uri(f'postgresql+psycopg2://{user}:{password}@{address}:5432/{dbname}')
        self.db_chain = SQLDatabaseChain(llm=self.llm, database=db, verbose=True)

    def llm_query(self, question):
        answer = self.llm(
            f'Table name = "sales_data". Table columns are {", ".join(self.data_columns)}. "EUROPE" column is boolean. Turn "{question}" into SQL query. Wrap the query in "```"')
        return self.llm(f'Extract the sql query from {answer} as simple string without quote')
        # answer = self.llm([HumanMessage(
        #     content=f'Table name = "sales_data". Table columns are {", ".join(self.data_columns)}. "EUROPE" column is boolean. Turn "{question}" into SQL query. Wrap the query in "```"')]).content
        # return self.llm([HumanMessage(content=f'Extract the sql query from {answer} as simple string without quote')]).content

    def chain(self, prompt, table_name):
        question = f"""
With table {table_name}, given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

{prompt}
"""
        return self.db_chain.run(question)


@st.cache_data
def prompt_to_query(prompt):
    return NaturalQuery(COLUMNS).llm_query(prompt).replace("'Y'", "True").replace("'N'", "False")


def query(query_text, conn=None):
    if conn is None:
        return duckdb.query(query_text).df()
    else:
        return pd.read_sql(query_text, con=conn)


c1, c2 = st.columns(2)

with c1:
    cloud_mode = st.checkbox('Are you running app on cloud or otherwise do you have no access to Postgresql?',
                             value=True)
with c2:
    if not cloud_mode:
        use_csv = st.checkbox('Use uploaded csv instead of existing Postgres table', value=True)
    else:
        use_csv = True

if use_csv:
    file = st.file_uploader('Upload sales_data.csv')
else:
    file = False
if not cloud_mode:
    # user = 'postgres'
    # password = '12345678'
    # dbname = 'test_20230706'
    # address = 'localhost'
    conn = sqlalchemy.create_engine(f'postgresql://{user}:{password}@{address}:5432/{dbname}')
else:
    conn = None

if file:
    sales_data = pd.read_csv(io.StringIO(file.read().decode('latin1')))
    sales_data['EUROPE'] = sales_data['TERRITORY'] == 'EMEA'
    sales_data.columns = [c.lower() for c in sales_data.columns]
    if not cloud_mode:
        from create_table import create_postgres_table
        create_postgres_table(sales_data, name='temp')
        # with psycopg2.connect(host=address,
        #                       port=5432,
        #                       database=dbname,
        #                       user=user,
        #                       password=password
        #                       ) as connection:
        #     with connection.cursor() as cursor:
        #         cursor.execute(f"CREATE SCHEMA IF NOT EXISTS public;")
        # sales_data.to_sql('sales_data', conn, schema='public', method=psql_insert_copy, if_exists='replace')

if (cloud_mode and file) or (not cloud_mode and (file or not use_csv)):
    # question = st.text_input('Input prompt')
    #
    # if len(question) > 0:
    #     answer = prompt_to_query(question)
    #     with st.expander('see SQL'):
    #         st.text(answer)
    #     st.dataframe(query(answer, conn=conn))

    with st.expander('unit tests'):
        for test_query in test_queries:
            if cloud_mode and file:
                answer = prompt_to_query(test_query).lstrip('"').rstrip('"')
                st.text(test_query)
                st.text(answer)
                try:
                    queried = query(answer, conn=conn)
                    st.dataframe(queried)
                    # st.text(OpenAI(model_name='gpt-3.5-turbo', openai_api_key=environ.Env()('OPENAI_API_KEY'))([HumanMessage(content=f'Explain following query result "{queried}"')]))

                except Exception as e:
                    st.text('prompt failed to convert to query')
                    st.text(e)
                st.divider()
            elif not cloud_mode and (file or not use_csv):
                table_name = 'temp' if not use_csv else 'sales_data'
                st.text(test_query)
                st.text(NaturalQuery(COLUMNS).chain(test_query, table_name=table_name))
                st.divider()

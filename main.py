import environ
import pandas as pd
import streamlit as st
from langchain import SQLDatabase, SQLDatabaseChain
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

from constants import *

st.set_page_config(page_title='Data Assistance Wizard')
environ.Env.read_env()


class NaturalQuery:
    def __init__(self,
                 llm=ChatOpenAI(model_name='gpt-3.5-turbo-16k', openai_api_key=environ.Env()('OPENAI_API_KEY'))):
        self.llm = llm

    def csv_run(self, prompt, df):
        return create_pandas_dataframe_agent(self.llm, df,
                                             verbose=VERBOSE,
                                             agent_type=AgentType.OPENAI_FUNCTIONS
                                             ).run(prompt)

    def db_run(self, prompt, db):
        return SQLDatabaseChain.from_llm(llm=self.llm,
                                         db=db,
                                         verbose=VERBOSE
                                         ).run(prompt)

def connect_to_db():
    try:
        import psycopg2
        db_info = f'{db_user}:{db_password}@{db_address}:{db_port}/{db_name}'
        st.session_state['db'] = SQLDatabase.from_uri(f'postgresql+psycopg2://{db_info}')
        # st.session_state['db_df'] = pd.read_sql(f'''SELECT * FROM {db_table_name} TABLESAMPLE SYSTEM_ROWS (40)''',
        #                                         con=sqlalchemy.create_engine(f'postgresql://{db_info}'))
    except Exception as e:
        print(e)
        st.session_state['db'] = None
        st.session_state['db_df'] = None
        st.session_state['failed_db'] = True


with st.sidebar:
    csv_encoding = st.text_input('csv_encoding', value=DEFAULT_ENCODING)
    csv_file = st.file_uploader('Upload csv')
    if st.session_state.get('failed_df', False):
        st.text('read csv failed, please check your file format and encoding')
        st.session_state['failed_df'] = False
    db_user = st.text_input('db_user', value=DB_USER)
    db_password = st.text_input('db_password', value=DB_PASSWORD)
    db_address = st.text_input('db_address', value=DB_ADDRESS)
    db_port = st.text_input('db_port', value=DB_PORT)
    db_name = st.text_input('db_name', value=DB_NAME)
    # db_table_name = st.text_input('db_table_name')
    db_connect = st.button('Connect', on_click=connect_to_db)
    if st.session_state.get('failed_db', False):
        st.text('connection to new database failed')
        st.session_state['failed_db'] = False

st.title('Data Assistance Wizard')
st.header('Ask questions about your data')

if csv_file:
    try:
        st.session_state['df'] = pd.read_csv(csv_file, encoding=csv_encoding)
    except:
        st.session_state['df'] = None
        st.session_state['failed_df'] = True

prompt = st.text_input('Prompt')
b1, b2 = st.columns(2)
with b1:
    if st.button('Ask about csv data'):
        if st.session_state.get('df', None) is not None:
            st.write(NaturalQuery().csv_run(prompt, st.session_state['df']))
        else:
            st.text('Error: no successful csv upload')
with b2:
    if st.button('Ask about Postgres data'):
        if st.session_state.get('db', None) is not None:
            st.write(NaturalQuery().db_run(prompt, st.session_state['db']))
        else:
            st.text('Error: no successful database connection')



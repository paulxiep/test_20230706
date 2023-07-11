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
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []


class NaturalQuery:
    def __init__(self,
                 llm=ChatOpenAI(model_name=MODEL_NAME, openai_api_key=environ.Env()('OPENAI_API_KEY'),
                                temperature=TEMPERATURE)):
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
        import psycopg2, sqlalchemy
        db_info = f'{db_user}:{db_password}@{db_address}:{db_port}/{db_name}'
        st.session_state['db'] = SQLDatabase.from_uri(f'postgresql+psycopg2://{db_info}')
        st.session_state['db_df'] = pd.read_sql(f'''SELECT * FROM {db_table_name}''',
                                                con=sqlalchemy.create_engine(f'postgresql://{db_info}'))
    except Exception as e:
        print(e)
        st.session_state['db'] = None
        st.session_state['db_df'] = None
        st.session_state['failed_db'] = True


def enter_password():
    if entered_password == environ.Env()('APP_PASSWORD'):
        st.session_state.unlocked = True


def clear_chat():
    st.session_state.chat_messages = []


if not st.session_state.get('unlocked', False):
    if environ.Env()('UNLOCKED') == 'yes':
        st.session_state.unlocked = True
    else:
        st.text('please find password in constants.py on github repo')
        entered_password = st.text_input('Enter app password')
        entering_password = st.button('Enter', on_click=enter_password)
else:
    with st.sidebar:
        data_source = st.radio('Ask about', options=['csv', 'postgres'])
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
        db_table_name = st.text_input('db_table_name')
        db_connect = st.button('Connect', on_click=connect_to_db)
        if st.session_state.get('failed_db', False):
            st.text('connection to new database failed')
            st.session_state['failed_db'] = False

        if csv_file:
            try:
                st.session_state['df'] = pd.read_csv(csv_file, encoding=csv_encoding)
            except:
                st.session_state['df'] = None
                st.session_state['failed_df'] = True

    st.title('Data Assistance Wizard')
    st.markdown("<div id='link_to_top'></div>", unsafe_allow_html=True)
    st.header('Ask questions about your data')

    prompt = st.chat_input('Ask something about your data')
    t1, t2 = st.tabs(['chat', 'preview'])
    with t1:
        for message in st.session_state.chat_messages:
            with st.chat_message(message['role']):
                st.write(message['content'])

        if prompt:
            st.session_state.chat_messages.append({'role': 'user', 'content': prompt})
            if data_source == 'csv':
                if st.session_state.get('df', None) is not None:
                    try:
                        response = NaturalQuery().csv_run(prompt, st.session_state['df'])
                    except Exception as e:
                        response = f'Failed to convert prompt to answer, try rewording.  \n  \n{e}'
                else:
                    response = 'Error: no successful csv upload'
            elif data_source == 'postgres':
                if st.session_state.get('db', None) is not None:
                    try:
                        response = NaturalQuery().db_run(prompt, st.session_state['db'])
                    except Exception as e:
                        response = f'Failed to convert prompt to answer, try rewording.  \n  \n{e}'
                else:
                    response = 'Error: no successful database connection'
            st.session_state.chat_messages.append({'role': 'assistant', 'content': response})
            st.session_state.tab = 'chat'
            st.experimental_rerun()
    with t2:
        with st.expander('csv preview'):
            st.dataframe(st.session_state.get('df', pd.DataFrame([[]])))

        with st.expander('postgres preview'):
            st.dataframe(st.session_state.get('db_df', pd.DataFrame([[]])))

    st.markdown("<a href='#link_to_top'>Back to top</a>", unsafe_allow_html=True)
    clear = st.button('clear chat history', on_click=clear_chat)

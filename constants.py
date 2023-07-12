# Model parameters
MODEL_NAME = 'gpt-4'
TEMPERATURE = 0
VERBOSE = False

# Because provided test case csv will fail with default or utf-8 encoding.
DEFAULT_ENCODING = 'latin1'

# DB connection parameters
DB_USER = 'postgres'
DB_PASSWORD = '12345678'
DB_NAME = 'test_20230706'
DB_ADDRESS = 'localhost'
DB_PORT = '5432'
DB_TABLE_NAME = 'sales_data'

# used for db_run, table name will be added to prompt to tell LLM to look at specific table
APPEND_TABLE_NAME_TO_PROMPT = True
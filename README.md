## test_20230706

Version Day 3

### What it is

 - A user-friendly web data application that allows users to ask questions about the data.

### Dependencies
 - Python 3.9+
 - With or without virtualenv, run ```pip install -r requirements.txt```.
 - If connection to SQL database is required, also run ```pip install -r db_requirements.txt```. (tested with Postgresql)
 - Requires .env file with ```OPENAI_API_KEY=YOUR_KEY_HERE```, ```UNLOCKED=yes```
 - App password is in place since a demo app is running on publicly-accessible cloud.
   - But this is not needed in the local version with ```UNLOCKED=yes``` set up properly.

### Usage Instructions
 - Start application with ```streamlit run main.py```
 - (if using csv data) Upload the input csv. The encoding might need to be manually configured.
 - (if using Postgresql) Set the connection details in the provided text boxes.
   - Or set the default values in constants.py
 - Different LLM models have different capabilities. This is set in constants.py
   - gpt-4 may be the most capable overall
   - gpt-3.5-turbo-16k may be needed to increase token limit
   - Temperature of 0 or close to it is advised so model doesn't make things up.
 - After uploading csv or establishing connection, previews will be available in preview tab.
 - Enter anything in the chat input box at the bottom.
 - Chat history is stored in the app, but not sent to the LLM, this is done considering token limit.
 - Clear chat history button is at the bottom on the chat tab.


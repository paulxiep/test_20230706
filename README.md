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
   - Each new prompt is a new LLM conversation.
 - Clear chat history button is at the bottom on the chat tab.

### Requirements
 - 2 main requirements are
   - To be able to ask questions about data in natural language and receive explained results.
     - In this and within the time limit of a few days, using ready-made API that connects LLM model directly to the data is the most practical.
       - Developing own pipeline was attempted, and deemed that it's not realistic to design a working pipeline in a few days.
       - But this leaves performance up to the capabilities of LLM to interpret questions and interact with the data and then explain that data.
   - To provide a user-friendly web-based interface or API.
     - It was decided that within a few days, learning and building a fully customizable web engine is not feasible.
     - So Streamlit, which I already know, and which is appropriate for data application, was chosen.
     - Streamlit is user-friendly enough for data practitioners, but for business users it remains a question.

### Implementation Details
 - Streamlit
   - Streamlit's primary design is that it always reruns code from top to bottom with any user interaction.
     - It used to be stateless too, meaning everything had to be reloaded and re-computed each time.
     - Statefulness has since been added to the tool.
       - But one still needs to be careful to design it to not redo expensive computations or API call.
 - App password
   - Since the same code is running on public cloud, application password is added to cloud env and required for cloud version
     - This is to prevent public usage of your API key
   - For local version, setting ```UNLOCKED=yes``` in .env is enough to allow access
 - Overall Design
   - Although potentially unnecessary, the app is designed to not persist any unnecessary object in memory.
     - Free cloud memory is 1 GB. This may be plenty for this use case, but testing time is short, I'm not taking any chances of the app failing due to memory.
     - So LLM and class objects are instantiated to perform its functions, then recycled away, functional programming style.
 - NaturalQuery
   - Though the Streamlit app calls it by creating new recyclable instances for each call, the Class is designed so that persisting Class Instance is a valid usage too.
     - So LLM engine is a Class attribute.
   - 2 methods
     - csv_run connects to the inputted pandas.DataFrame object
     - db_run connects to the pre-connected Database connection

### Known Issues
 - If csv is poorly formatted, the app will fail at csv upload.
   - LLM is not yet involved in csv load, which still uses ```pd.read_csv()```
 - LLM may be capable of interpreting column names and data, or may not.
   - Getting accurate answers or any answer at all relies on the capabilities of the LLM.
   - Sometimes rewording the question can get the correct answer if the original one cannot.
   - In the provided test data, asking to list European or non-European countries will succeed, but asking to list Asian countries will return nothing.
   - Potentially there are more potential issues with LLM ability to get correct answers, but testing them require API calls.
     - Assuming each API call is billed, I decided not to do it more than I already have, to save you money.
 - Any database system other than Postgres was not tested, and even Postgres was tested only on my configurations.
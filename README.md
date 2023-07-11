## test_20230706

Version Day 2

#### Assumptions

 - Python version required is 3.9+
 - .env with the right secrets should be in the working directory if running local.

#### Notes

 - For local run, use command ```streamlit run main.py```
 - On Day 2 (today) I found Langchain's dataframe API, so now the csv and postgres versions have roughly the same capabilities.
 - Postgres connection won't work on Streamlit cloud demo, but won't crash the App.
 - Chatgpt is a bit unpredictable, for example:
   - 'Total quantity for each product line' will be executed successfully.
   - but 'Total orders for each product line' will fail.
 - On Day 3 I'll experiment with model temperature to see if it helps, or maybe something else too.
 - I tried to integrate data preview feature, but it will be pushed to Day 3.
 - Chat history is a planned feature for Day 3.
 - Currently the app is in development, so I try to use the latest version of libraries possible.
 - Only in established apps will I start fixing library versions.
 - requirements.txt is for cloud version. Additional requirements for local version with Postgresql is in db_requirements.txt
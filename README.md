## test_20230706

#### Assumptions

 - Postgres database variables (password, dbname, etc.) used are in *constants.py*.
 - .env with the right secrets should be in working directory if running local.

#### Notes

 - Currently in the unit test stage, prompts are fixed and are listed in unit_tests.py
 - Unit test results are under expander.
 - Currently the app is in development, so I try to use the latest version of libraries possible.
 - Only in established apps will I start fixing library versions.
 - requirements.txt is for cloud version. Additional requirements for local version with Postgresql is in db_requirements.txt
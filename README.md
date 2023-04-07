# flask-school-project
A flask application that handles authentication and file upload

# How to run the application

## Setting up virtual environment and installing required packages
* Clone the app using git or download zip file
* In the root folder, create a virtual environment by typing "python -m venv virtual" in the terminal
* Activate the environment by typing "virtual\Scripts\activate"
* Install required packages in requirements.txt file by typing "pip install requirements.txt"

## Connect to MySQL and create user model
* Open app.py
* Input MySQL password in app.config['MYSQL_PASSWORD']
* Input Schema name in app.config['MYSQL_DB'] (mine is 449_db)
* Open MySQL workbench and runs users.sql file in models folder to create a new db and insert admin account

## Run the app
* In the terminal, type "python app.py" to start the app

# Team member: 1 member
* Phu Nguyen


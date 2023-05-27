# Install MySQL on your computer from
# https://dev.mysql.com/downloads/installer/
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python

import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'mysql7'
)

# create a DB cursor
cursorObject = dataBase.cursor()

# create a DB
cursorObject.execute("CREATE DATABASE dogshelterdb")

print("DB Successfully created")
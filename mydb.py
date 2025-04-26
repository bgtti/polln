# Install MySQL if you do not have it: https://www.w3schools.com/mysql/mysql_install_windows.asp#:~:text=The%20simplest%20and%20recommended%20method,%2D8.0.23.msi%20.
# pip install mysql
# pip install mysql-connector-python
# IF THE PREVIOUS CONNECTOR DOES NOT WORK, USE: pip install mysql-connector
# now run on your terminal: python mydb.py
# if "Db set up!" appears on your terminal, all worked well
# A video on how to set up django with mySQL is available here: https://www.youtube.com/watch?v=t10QcFx7d5k

import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

dataBase = mysql.connector.connect(
    host='localhost',
    user=os.environ.get('MYSQL_USER'),
    passwd=os.environ.get('MYSQL_PASSWORD'),
)

# prepare a cursor object
cursorObject = dataBase.cursor()

# create db
cursorObject.execute("CREATE DATABASE pollnmysql")

print("Db set up!")

'''
Name: SQL_Connector
Description: This file uses mysql connector python to link mysql with python along with specific database access
Developer: Seema Suresh
'''
from mysql.connector import (connection)

cnx = connection.MySQLConnection(user='root', password='p@ssw0rd',host='127.0.0.1', port ='3306',database='heap')
cnx.close()
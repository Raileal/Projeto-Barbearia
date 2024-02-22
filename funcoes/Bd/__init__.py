import mysql.connector

def configure_mysql_connection():
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="7319",
        )
        return mydb
    except mysql.connector.Error:
        return None
    
def create_database():
    mybd = configure_mysql_connection()
    cursor = mybd.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Barber")

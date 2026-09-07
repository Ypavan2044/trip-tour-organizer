import pymysql

def create_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Pavan@2004",
        database="trip_organizer",
        autocommit=False
    )
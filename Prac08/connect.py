import psycopg2
import config       
def connect():
    try:
        conn = psycopg2.connect(
            host = config.host,
            database = config.database,
            user = config.user,
            password = config.password,
        )
        print("connection succesful")
        return conn
    except Exception as e:
        print("connection error:" , e)
connect()

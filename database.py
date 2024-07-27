import psycopg2 as db


class Database:
    def __init__(self):
        self.conn = None
        self.c = None

    def connection(self, dbname, user, password, host='127.0.0.1', port='65432'):
        try:
            self.conn = db.connect(dbname=dbname, user=user, password=password, host=host, port=port)
            self.c = self.conn.cursor()
            print("Connected to database.")
        except db.DatabaseError as e:
            print(f"Can't connect - error: {e}")

    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS logsSystem (
                    Flight_No INT UNIQUE,
                    status VARCHAR,
                    x INT,
                    y INT,
                    z INT)"""
        try:
            self.c.execute(query)
            self.conn.commit()
            print("Table - success")
        except db.DatabaseError as e:
            print(f"Table - failure: {e}")
        finally:
            if self.c is not None:
                self.c.close()
            if self.conn is not None:
                self.conn.close()


database = Database()
database.connection(dbname='AirportProject', user='db', password='db', host='127.0.0.1', port='65432')
database.create_table()

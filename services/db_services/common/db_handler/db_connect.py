import psycopg2
from psycopg2 import sql

class DatabaseConnector:
    def init(self, dbname, user, password, host='localhost', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Database connection established.")
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        if not self.connection:
            raise Exception("Connection is not established. Call connect() first.")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                print("Query executed successfully.")
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            raise

    def fetch_results(self, query, params=None):
        if not self.connection:
            raise Exception("Connection is not established. Call connect() first.")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return results
        except psycopg2.Error as e:
            print(f"Error fetching results: {e}")
            raise

# Example usage:
# db = DatabaseConnector(dbname="mydb", user="myuser", password="mypassword")
# db.connect()
# db.execute_query("CREATE TABLE test (id SERIAL PRIMARY KEY, name VARCHAR(50));")
# db.close()
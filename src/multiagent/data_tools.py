import duckdb
from agents import function_tool

class DataTools:
    def __init__(self):
        self.connection_string = "./db/main.duckdb"

    @function_tool()
    def execute_query(self, query):
        connection_string = "./db/main.duckdb"
        with duckdb.connect(connection_string) as db:
            try:
                result = db.execute(query).fetchall()
                return result
            except Exception as e:
                print(e)
                raise e

    def get_schema(self):
        with open("./scripts/01_ddl.sql", "r", encoding="utf-8") as r:
            schema = r.read()
        return schema
    


"""
        self.connection_string="./db/main.duckdb"
        with duckdb.connect(self.connection_string) as db:
            schema = db.execute(
                                  SELECT table_name,
                                         column_name,
                                         data_type,
                                         is_nullable
                                  FROM information_schema.columns
                                  WHERE table_schema = 'main'
                                  ORDER BY table_name, ordinal_position
                                  ).fetchall()
"""



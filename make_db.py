import duckdb
from load_data import load_vitacress_1, load_vitacress_2, load_flavourfresh_1, load_flavourfresh_2

''' Loads the trials dataframes into the database. '''

def create_db():
    # Create a connection to a DuckDB database file
    conn = duckdb.connect(':memory:')

    for tablename, loader in {'vitacress_1': load_vitacress_1, 
                'vitacress_2': load_vitacress_2, 
                'flavourfresh_1': load_flavourfresh_1,
                    'flavourfresh_2': load_flavourfresh_2}.items():
        df = loader()
        # Write the Polars DataFrame to a DuckDB table
        conn.execute(f"CREATE TABLE {tablename} AS SELECT * FROM df")
    return conn
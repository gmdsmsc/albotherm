import polars as pl
import streamlit as st
import plotly.express as px
from make_db import create_db

import subprocess

result = subprocess.run(['./install.sh'])

conn = create_db()

TABLES = {'Vitacress 1': 'vitacress_1', 
          'Vitacress 2': 'vitacress_2', 
          'Flavourfresh 1': 'flavourfresh_1', 
          'Flavourfresh 2': 'flavourfresh_2'}

# Define functions for your pages
def load_page(display_name):
    tablename = TABLES[display_name]
    st.title(display_name)
    # Load data for Page 1
    df = load_table(tablename)
    sensor_columns = [col for col in df.columns if col != 'DateTime']
    fig = px.line(df, x='DateTime', y=sensor_columns)
    st.plotly_chart(fig)


# Functions to load data into a polars dataframe
def load_table(tablename):
    cursor = conn.cursor()
    # Ensure the table name is treated safely to prevent SQL injection
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tablename,))
    if not cursor.fetchone():
        raise ValueError("Table does not exist.")
    query = f"SELECT * FROM {tablename}"
    cursor.execute(query)
    df = cursor.fetch_arrow_table().to_pandas()
    return pl.DataFrame(df)

# Add a selectbox to the sidebar for navigation
page = st.sidebar.selectbox("Choose a page:", TABLES.keys())
load_page(page)

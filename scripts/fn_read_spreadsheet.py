import streamlit as st
import pandas as pd
from scripts.fn_connect_to_spreadsheet import fn_connect_to_spreadsheet

# Variables
date_format_in_spreadsheet = "%d/%m/%Y %H:%M:%S"

### READ SPREADSHEET ###
@st.experimental_memo(ttl=600)
def fn_read_spreadsheet():
    # Connect to spreadsheet
    sh = fn_connect_to_spreadsheet()
    sheet_name = 'flightDataset'
    # Read worksheet
    worksheet = sh.worksheet(sheet_name)
    df = pd.DataFrame(worksheet.get_all_records())
    df = df[~(df['Flight Number'].isin(['#VALUE!']))] # filter out rows without data
    df['Destination Start Time'] = pd.to_datetime(df['Destination Start Time'], format=date_format_in_spreadsheet)
    df['Destination End Time'] = pd.to_datetime(df['Destination End Time'], format=date_format_in_spreadsheet)
    df['Event Start Date'] = pd.to_datetime(df['Event Start Date'], format="%d/%m/%Y").dt.date
    df['Event End Date'] = pd.to_datetime(df['Event End Date'], format="%d/%m/%Y").dt.date

    return df
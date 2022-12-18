import streamlit as st
from gspread_pandas import Spread,Client
from google.oauth2 import service_account

def fn_connect_to_spreadsheet():
    ### Create a connection to spreadsheet ###
    scope = ["https://www.googleapis.com/auth/spreadsheets"
            ,"https://spreadsheets.google.com/feeds"
            ,"https://www.googleapis.com/auth/drive"]
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    client = Client(scope=scope, creds=credentials)
    spreadsheet_name = 'py_flight_data'
    sheet_name = 'flightDataset'
    spread = Spread(spreadsheet_name, client = client)

    # Call our spreadsheet
    sh = client.open(spreadsheet_name)
    # worksheet_list = sh.worksheets()
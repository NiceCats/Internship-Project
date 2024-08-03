import streamlit as st
import pandas as pd
import numpy as np
import plotly as pl
import plotly.express as px
import plotly.graph_objects as go
import numerize.numerize as numerize
import os

# title for streamlit
st.title("Submit Data Excel")

# upload file type xlsx and csv
uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "csv"])

# read file
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df = df.copy()
    st.write(df)
    
    save_path = "data"
    os.makedirs(save_path, exist_ok=True)
    with open (os.path.join(save_path, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    # columns order data file
    column_order = ["Nama Nasabah", "Jenis Sampah", "Jumlah", "Harga", 
                    "Total Harga", "Total Keseluruhan", "Wilayah", "Bulan", "Tahun"]
    
    if list (df.columns) != column_order:
        invalid_order = set(df.columns) - set(column_order)       
        st.error(f"Column order is invalid. Please use the following order: {column_order}. Invalid columns: {', '.join(invalid_order)}")
        
st.divider()

# chart type
st.sidebar.header("Please Select:")
if 'df' in locals() or 'df' in globals():
    unique_columns = st.sidebar.selectbox(
    "Select Column:",
    options = df.columns.unique().tolist(),
)
    
    unique_months = st.sidebar.multiselect(
        "Select Month:",
        options = df["Bulan"].unique().tolist(),
    )
    
    unique_years = st.sidebar.selectbox(
        "Select Year:",
        options = df["Tahun"].unique().tolist(),
    )
else:
    st.warning("Please upload a file to proceed.")
    
# pie chart
if 'df' in locals() or 'df' in globals() and unique_columns == "Nama Nasabah":
    filtered_df = df[(df["Bulan"].isin(unique_months)) & (df["Tahun"] == unique_years)]
    fig = px.pie(filtered_df, names=unique_columns, values='Total Keseluruhan', title='Pie Statistics by Total Keseluruhan')
    st.plotly_chart(fig)

    filtered_df = df[(df["Bulan"].isin(unique_months)) & (df["Tahun"] == unique_years)]
    fig = px.bar(filtered_df, x = unique_columns, y = "Total Harga", title = 'Bar Chart by Total Harga')
    st.plotly_chart(fig)
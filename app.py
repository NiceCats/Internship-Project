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

def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df

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
if 'df' in locals() or 'df' in globals():
    st.sidebar.header("Please Select Options:")
    
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
    st.warning("Please upload .xlsx or .csv file to proceed.")
    
# pie chart
if 'df' in locals() or 'df' in globals():
    filtered_df = df[(df["Bulan"].isin(unique_months)) & (df["Tahun"] == unique_years)]
    fig_pie_nasabah = px.pie(
        filtered_df, 
        names=unique_columns, 
        values='Total Keseluruhan',
        hole=0.4,
        title="<b>Pie Chart by Nama Nasabah</b>"
    )
    st.plotly_chart(fig_pie_nasabah)

    fig_bar_totalharga = px.bar(
        filtered_df,
        x = unique_columns,
        y = "Total Harga",
        orientation = "v",
        title = "<b>Bar Chart by Total Harga</b>",
        template = "plotly_white"
    )
    fig_bar_totalharga.update_layout(
        xaxis = dict(showgrid = False),
    )
    st.plotly_chart(fig_bar_totalharga)
    
    if "Nama Nasabah" in unique_columns:    
        fig_line_totalharga = px.line(
            df,
            x = "Nama Nasabah",
            y = "Total Keseluruhan",
            title = "<b>Line Chart by Total Harga</b>"
        )
        st.plotly_chart(fig_line_totalharga)
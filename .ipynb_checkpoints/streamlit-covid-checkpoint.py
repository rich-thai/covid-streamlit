import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import altair as alt
import plotly.express as px



st.title('COVID-19 Ontario')

url="https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv"
df=pd.read_csv(url)

df["Daily Deaths"]=df["Deaths"].diff()
df["Daily Cases"]=df["Total Cases"].diff()
df["Daily Positivity Rate"]=np.round(df["Daily Cases"]/df["Total tests completed in the last day"]*100,1)
df['Positivity % (7 day avg)'] = np.round(df["Daily Positivity Rate"].rolling(window=7).mean(),2)

if st.checkbox('Show raw data'):
    st.subheader('Raw data (last 100)')
    st.write(df.tail(100))

# st.text(df.columns.values)
st.subheader('As of ' + df.iloc[-1]['Reported Date'] + ':')
st.write(df.iloc[-1][['Daily Deaths','Daily Cases','Daily Positivity Rate','Total tests completed in the last day','Confirmed Positive','Resolved','Deaths','Total Cases', 'Under Investigation','Number of patients hospitalized with COVID-19','Number of patients in ICU with COVID-19']])

fig = px.line(df, x='Reported Date', y='Daily Cases', title='Daily Cases')
st.plotly_chart(fig, use_container_width=True)

fig = px.line(df, x='Reported Date', y='Positivity % (7 day avg)', title='Positivity % (7 day avg)')
st.plotly_chart(fig, use_container_width=True)


fig = px.line(df, x='Reported Date', y='Number of patients hospitalized with COVID-19', title='Number of patients hospitalized with COVID-19')
st.plotly_chart(fig, use_container_width=True)

fig = px.line(df, x='Reported Date', y='Number of patients in ICU with COVID-19', title='Number of patients in ICU with COVID-19')
st.plotly_chart(fig, use_container_width=True)


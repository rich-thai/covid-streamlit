import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


st.title('COVID-19 Ontario')

url="https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv"
url2 = 'https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv'

df=pd.read_csv(url)
df2 = pd.read_csv(url2).rename(columns={'Reporting_PHU_Latitude':'lat','Reporting_PHU_Longitude':'lon'})

df["Daily Deaths"]=df["Deaths"].diff()
df["Daily Cases"]=df["Total Cases"].diff()
df["Daily Positivity Rate"]=np.round(df["Daily Cases"]/df["Total tests completed in the last day"]*100,1)
df['Positivity % (7 day avg)'] = np.round(df["Daily Positivity Rate"].rolling(window=7).mean(),2)
df.rename(columns={'Number of patients hospitalized with COVID-19':'Patients hospitalized with COVID-19','Number of patients in ICU with COVID-19':'Patients in ICU with COVID-19'}, inplace=True)

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data (last 100)')
#     st.write(df.tail(100))
    
# if st.checkbox('Show raw data 2'):
#     st.subheader('Raw data (last 100)')
#     st.write(df2[df2.Case_Reported_Date>'2020-10-01'])
    
today = df.iloc[-1]['Reported Date']  
st.subheader('Last updated: ' + today)

 
yesterday = datetime.now() - timedelta(8)


st.write(df.iloc[-1][['Daily Deaths','Daily Cases','Daily Positivity Rate','Total tests completed in the last day','Confirmed Positive','Resolved','Deaths','Total Cases', 'Under Investigation','Patients hospitalized with COVID-19','Patients in ICU with COVID-19']])

dayslider = st.radio(
     "Past # of days",
     (1, 7, 30))


datefilter = yesterday = datetime.now() - timedelta(dayslider)


df2filt = df2[df2.Case_Reported_Date>=datetime.strftime(datefilter, '%Y-%m-%d')]\
    .groupby(by=['lat','lon', 'Reporting_PHU']).agg({'Row_ID':'count'})\
    .reset_index().rename(columns={'Row_ID':'Count'})\
    .sort_values(by='Count', ascending=False)
df2filt['Reporting_PHU'] = df2filt['Reporting_PHU']\
    .str.replace('Public','')\
    .str.replace('Health','')\
    .str.replace('Unit','')\
    .str.replace('Department','')\
    .str.replace('Services','')

st.markdown('Cases reported in the last week:')
st.write(df2filt[['Reporting_PHU', 'Count']])


fig = go.Figure(go.Bar(
            x=df2filt['Count'],
            y=df2filt['Reporting_PHU'],
            orientation='h'))
fig.update_layout(
    xaxis_title='Cases in the last ' + str(dayslider) +  ' day(s)',
    width=100,
    height=500
)
fig.update_yaxes(automargin=True)
st.plotly_chart(fig, use_container_width=True)

pie_df = df2[df2.Case_Reported_Date>=datetime.strftime(yesterday, '%Y-%m-%d')].groupby(by='Age_Group').agg({'Row_ID':'count'}).rename(columns={'Row_ID':'Count'}).reset_index()


fig = px.pie(pie_df, values='Count', names='Age_Group', title='Cases Among Age Groups (last ' + str(dayslider) +  ' day(s))')
st.plotly_chart(fig, use_container_width=True)

# st.text(df.columns.values)

st.subheader('Line Graphs')

fig = px.line(df, x='Reported Date', y='Daily Cases', title='Daily new cases')
st.plotly_chart(fig, use_container_width=True)

fig = px.line(df, x='Reported Date', y='Positivity % (7 day avg)', title='Positivity % (7 day avg)')
st.plotly_chart(fig, use_container_width=True)

fig = px.line(df, x='Reported Date', y=['Confirmed Positive','Patients hospitalized with COVID-19'], title='Comparing active and hospitalized cases')

fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="right",
    x=0.75
))

st.plotly_chart(fig, use_container_width=True)

fig = px.line(df, x='Reported Date', y=['Patients hospitalized with COVID-19','Patients in ICU with COVID-19'], title='Comparing hospitalized and in-ICU cases')

fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="right",
    x=0.75
))

st.plotly_chart(fig, use_container_width=True)

# st.map(df2)

# fig = px.scatter_geo(df2filt, lat='lat', lon='lon',
#                      size="Count",
#                      hover_name='Reporting_PHU',
#                      labels={'Row_ID'},
#                      text='Count'
#                      )
# fig.update_layout(mapbox_style="open-street-map")
# st.plotly_chart(fig, use_container_width=True)

fig = px.line(df, x='Reported Date', y='Daily Deaths', title='Daily Deaths')

st.plotly_chart(fig, use_container_width=True)
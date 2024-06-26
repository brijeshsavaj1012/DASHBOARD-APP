import streamlit as st 
import pandas as pd 
import numpy as np 
import datetime
import plotly.express as px 
import plotly.graph_objects as go

df = pd.read_csv('MOTOR-VEHICLE-CRASH.csv')
df['CRASH DATE'] = pd.to_datetime(df['CRASH DATE'])

df['CRASH DATE'] = pd.to_datetime(df['CRASH DATE'])
df['year'] = df['CRASH DATE'].dt.year
df['month'] = df['CRASH DATE'].dt.month
df['time'] = pd.to_datetime(df['CRASH TIME'])
df['time'] = [time.time() for time in df['time']]
df['time_cat'] = ['DAY' if time.hour > 6 else 'NIGHT' for time in df['time']] 

st.set_page_config(layout="wide", page_title="DASHBOARD", page_icon=":taxi:")

st.markdown("<h1 style='text-align: center; '>MOTOR VEHICLE CRASH ANALYSIS OF NYC</h1>", unsafe_allow_html=True)

col1, col2 = st.columns((1, 1.5))

col_names = ['NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED',
       'NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF PEDESTRIANS KILLED',
       'NUMBER OF CYCLIST INJURED', 'NUMBER OF CYCLIST KILLED',
       'NUMBER OF MOTORIST INJURED', 'NUMBER OF MOTORIST KILLED']

col_name = 'NUMBER OF PERSONS INJURED'

with col1:
    
    option1 = st.selectbox(
    'BAR AND RADAR',
    col_names)
    
    temp = df.groupby(['year']).sum()
    temp['year'] = temp.index
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=temp['year'], y=temp[option1],
                        mode='lines+markers',
                        name = option1,
                        line=dict(color='firebrick', width=5, dash='dash'))
                        )
    
    fig.add_trace(go.Bar(x=temp['year'], y=temp[option1],
                         name = option1
                        ))
    
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='black',
                      marker_line_width=3, opacity=0.8)
    
    fig.update_layout(
        autosize=False,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            
        ),
        margin=dict(l=30, r=30, t=30, b=30),
        height = 400,
        width = 550
    )
        
    
    st.plotly_chart(fig)
    
    
    temp_df2 = df.groupby(['BOROUGH', 'year']).sum()
    temp_df2 = temp_df2.reset_index(level=['BOROUGH','year'])
    
    fig4 = px.bar_polar(temp_df2, r=option1, theta='BOROUGH',
                    animation_frame = 'year')

    fig4.update_traces(marker_color='rgb(158,202,225)', marker_line_color='black',
                      marker_line_width=3, opacity=0.7)
    fig4.update_layout(
        autosize=False,
        margin=dict(l=30, r=30, t=30, b=30),
        height = 500,
        width = 520
    )
    st.plotly_chart(fig4)
    
    option4 = st.selectbox('PIE CHART', col_names)
    
    temp_df_7 = df.groupby(['CONTRIBUTING FACTOR VEHICLE 1']).sum().sort_values(by = option4, ascending = False)[1:15]
    temp_df_7['CONTRIBUTING FACTOR VEHICLE 1'] = temp_df_7.index
    fig1 = px.pie(temp_df_7, values=option4, names='CONTRIBUTING FACTOR VEHICLE 1', title='TOP 15 CONTRIBUTING FACTORS FOR INCIDENTS', hole=.5)
    fig1.update_layout(
        autosize=False,
        margin=dict(l=30, r=30, t=30, b=30),
        height = 500,
        width = 550
    )
    st.plotly_chart(fig1)
    
    st.markdown("""
    <style>
    .big-font {
        font-size:40px !important;
    }
    .small-font {
        font-size:55px; 
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="small-font"><b>TOP 10 <br> ON STREET NAME <br> INCIDENT ARE OCCURED</b></p>', unsafe_allow_html=True)


 
with col2:
    option2 = st.selectbox('MAPBOX', col_names)
    map_df = df[df[option2] >= 1]
    fig2 = px.scatter_mapbox(map_df, lat="LATITUDE", lon="LONGITUDE", animation_frame="year", color_continuous_scale=px.colors.cyclical.IceFire, color=option2, zoom=9, mapbox_style='carto-positron', center=dict(lon=-73.962870, lat=40.676403))
    fig2.update_mapboxes(pitch=35)
    fig2.update_layout(margin=dict(l=30, r=30, t=30, b=40),height = 800, width = 750, coloraxis_showscale=False)
    st.plotly_chart(fig2)
    

    temp_df3 = df.groupby(['BOROUGH', 'year', 'time_cat']).sum()
    temp_df3 = temp_df3.reset_index(level=['BOROUGH', 'year', 'time_cat'])
    
    option5 = st.selectbox('ICICLE CHART', col_names)

    fig3 = px.icicle(
       temp_df3,
       path=[px.Constant("DEATH-IN-NEW-YORK-AREAS"),'BOROUGH', 'year', 'time_cat'],
       values = option5,
       width=500, height=400
       
    )
    fig3.update_layout(
        autosize=False,
        margin=dict(l=30, r=30, t=30, b=30),
        height = 530,
        width = 750
    )
    
    fig3.update_traces(root_color="lightgrey")
    st.plotly_chart(fig3)
    
    option3 = st.selectbox('BUBBLE CHART', col_names)
    
    temp_df_6 = df.groupby('ON STREET NAME').sum().sort_values(by = option3, ascending = False)
    temp_df_6 = temp_df_6[1:10]
    temp_df_6['ON STREET NAME'] = temp_df_6.index
    
    fig5 = go.Figure(data=[go.Scatter(
        x=temp_df_6['ON STREET NAME'], y=temp_df_6[option3],
        mode='markers',
        marker_size=(temp_df_6[option3]/temp_df_6[option3].sum())*450,
        marker = dict(color=[120, 125, 130, 135, 140, 145, 160, 180, 190],)
    )])
    
    fig5.update_traces(marker_line_color='rgb(0,0,0)', marker_line_width=3, opacity=1)
    fig5.update_layout(
        autosize=False,
        margin=dict(l=30, r=30, t=30, b=30),
        height = 500,
        width = 815
    )
    
    st.plotly_chart(fig5)

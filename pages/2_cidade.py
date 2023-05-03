from haversine import haversine
import plotly.express as px
import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
import matplotlib.pyplot as plt
import os

df = pd.read_csv(f"./dataset/new_dataset.csv")

st.set_page_config( page_title= "Visão Empresa", layout = 'wide')
# Agrupamemnto s/ condição
def count_grouped(df, cols, agrouped, by, ascending):
   
    df_aux = df.loc[:, cols].groupby(agrouped).count()\
                            .sort_values(by = by, ascending = ascending).reset_index()
    df_aux = df_aux.iloc[0,1]
    
    return df_aux


def count_grouped_onecondition(df, variable, condition,cols, agrouped, by, ascending):
    df_aux = df.loc[df[variable] == condition, cols].groupby(agrouped)\
                                                    .count()\
                                                    .sort_values(by = by, ascending = ascending)\
                                                    .reset_index()
    df_aux = df_aux.iloc[0,1]
    
    return df_aux


def mean_grouped(df, cols, agrouped, by, ascending):
   
    df_aux = df.loc[:, cols].groupby(agrouped).mean()\
                            .sort_values(by = by, ascending = ascending).reset_index().round(2)
    df_aux = df_aux.iloc[0,1]
    
    return df_aux


def mean_grouped_onecondition(df, variable, condition,cols, agrouped, by, ascending):
    df_aux = df.loc[df[variable] == condition, cols].groupby(agrouped)\
                                                    .mean()\
                                                    .sort_values(by = by, ascending = ascending)\
                                                    .reset_index()
    df_aux = df_aux.iloc[0,1]
    
    return df_aux

def country_maps(df):
    cols = ['country code','latitude','longitude']
    df_aux = df.loc[:, cols].groupby(['country code'])['latitude','longitude'].median().reset_index()

    map = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['latitude'], location_info['longitude']],
                        popup= [location_info[['country code']]]).add_to(map)

    folium_static(map, width = 1024, height = 600)


df['latitude'] =df['latitude'].round(3)
df['longitude'] = df['longitude'].round(3)

# --- Menu ----

image_file = os.path.join('pages', 'zomatologo.png')
image = Image.open(image_file)

st.sidebar.image(image, width=240)

st.sidebar.markdown('## Zomato')
st.sidebar.markdown("---")

st.write('# Zomato KPI Dashboard - Cidade')

# ----- Filters -----
paises = list(df['country code'].unique())
precos = list(df['price category'].unique())
culinaria = list(df['cuisines'].unique())


# ========================================
# Filtro
# ========================================

pais = st.sidebar.multiselect('Países para análise:',
                                     paises,
                                     default = ['Brazil', 'Australia', 'England'])

st.sidebar.write("---")

slider_rate = st.sidebar.slider('Avaliação: ',0, 5,(5)) #sincronizar com o df

culinaria = st.sidebar.multiselect('Culinária:',
                                     culinaria,
                                     default = ['Italian','Arabian','Cafe'])


st.sidebar.write("---")


# filtro de data 
linhas_selecionadas = df['country code'].isin(pais)
df = df.loc[linhas_selecionadas, :]

# filtro de data 
linhas_selecionadas = df['price category'].isin(precos)
df = df.loc[linhas_selecionadas, :]

#filtro de data 
df = df.loc[df['aggregate rating'] <= slider_rate,:]

# =====================================
#               Layout
# =====================================
# 
with st.container():
    st.markdown('### Quantidade de restaurantes por cidade')
    df_aux = df.loc[:, ['restaurant name','city','country code']].groupby('city')['restaurant name'].count().reset_index().sort_values(by ='restaurant name', ascending = False).head(10)
    fig = px.bar(df_aux, x = 'city',y = 'restaurant name', color = 'city')
    
    st.plotly_chart(fig , use_container_width= True)
  


with st.container():
    st.markdown('#### Quantidade tipos de culinária  por cidade')
    cuisines_city = df.loc[:, ['cuisines', 'city']].groupby('city').nunique().reset_index().sort_values(by= 'cuisines', ascending = False).head(10)
    fig = px.bar(cuisines_city, 'city','cuisines', color= 'cuisines')
    st.plotly_chart(fig, use_container_width= True)

with st.container():
    st.write("---")
    col1, col2 = st.columns(2)
    
    with col1:
        cols = ['city', 'restaurant id']
        agrouped = 'city'
        by = 'restaurant id'
        df1 = df.loc[:, cols].groupby(agrouped)['restaurant id'].count().reset_index()

        df2 = df.loc[:, ['city', 'aggregate rating']].groupby('city')['aggregate rating'].mean().reset_index()
        
        df3 = pd.merge(df1, df2, on = 'city')
        df3 = df3.reindex(columns = ['country code','city','restaurant id','aggregate rating'])
        df3.columns = ['Country','City','Count Restaurant','Avg Rating']

        st.markdown('#### Métrica Geral')
        st.dataframe(df3, use_container_width= True)
    
    with col2: 
        #1) agrupamento de culinaria
        cuisines_city = df.loc[:, ['cuisines', 'city']].groupby('city').nunique().reset_index()

        #2) agrupamento de reservas de mesas 
        cols = ['city', 'has table booking']
        agrouped = 'city'
        by = 'has table booking'
        booking_table = df.loc[:,cols].groupby(agrouped).count().reset_index()

        #4) 
        cols = ['city','has online delivery']
        agrouped = 'city'
        by = 'has online delivery'
        online_delivery = df.loc[:,cols].groupby(agrouped).count().reset_index()

        merged1 = pd.merge(cuisines_city, booking_table, on = 'city')
        merged2 = pd.merge(merged1, online_delivery, on = 'city')
        st.markdown('#### Métricas de serviço')
        st.dataframe(merged2, use_container_width= True)

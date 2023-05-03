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

df = pd.read_csv(r'C:\Users\guga1\OneDrive\Documentos\repos\zomato_restaurants\dataset\new_dataset.csv')

st.set_page_config( page_title= "Visão Empresa", layout = 'wide')
# Agrupamemnto s/ condição
def count_grouped(df, cols, agrouped, by, ascending):
   
    df_aux = df.loc[:, cols].groupby(agrouped).count()\
                            .sort_values(by = by, ascending = ascending).reset_index()
    
    
    return df_aux


def count_grouped_onecondition(df, variable, condition,cols, agrouped, by, ascending):
    df_aux = df.loc[df[variable] == condition, cols].groupby(agrouped)\
                                                    .count()\
                                                    .sort_values(by = by, ascending = ascending)\
                                                    .reset_index()
    
    
    return df_aux


def mean_grouped(df, cols, agrouped, by, ascending):
   
    df_aux = df.loc[:, cols].groupby(agrouped).mean()\
                            .sort_values(by = by, ascending = ascending).reset_index().round(2)
    
    
    return df_aux


def mean_grouped_onecondition(df, variable, condition,cols, agrouped, by, ascending):
    df_aux = df.loc[df[variable] == condition, cols].groupby(agrouped)\
                                                    .mean()\
                                                    .sort_values(by = by, ascending = ascending)\
                                                    .reset_index()
    
    
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
df['average cost for two (usd)'] = df['average cost for two (usd)'].round(2)
# --- Menu ----

image_file = os.path.join('pages', 'zomatologo.png')
image = Image.open(image_file)

st.sidebar.image(image, width=240)

st.sidebar.markdown('## Zomato')
st.sidebar.markdown("---")

st.write('# Zomato KPI Dashboard - Restaurants')

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

# ==================================================================
#                   Layout
# ==================================================================

with st.container():
    st.markdown(' ## Melhores Restaurantes - Avaliação')
    rating_by_restaurants = df.loc[:, ['restaurant name','aggregate rating','city']].groupby(['restaurant name']).mean().sort_values(by = 'aggregate rating', ascending = False).head(10)
    fig = px.bar(rating_by_restaurants)
    st.plotly_chart(fig, use_container_width= True)
    # st.dataframe(rating_by_restaurants)

with st.container():
    st.markdown(' ## Opções de Culinarias')
    cuisines_type = df['cuisines'].value_counts().head(10)
    fig = px.bar(cuisines_type)
    st.plotly_chart(fig, use_container_width= True)

with st.container():
    st.write("---")
    st.markdown(" ## Métricas")
    st.write("\n")
    st.write("\n")
    col1, col2  = st.columns(2)
    
    with col1:
        count_restaurant_rating = count_grouped(df, ['restaurant name','aggregate rating','country code'], ['country code','restaurant name'], 'aggregate rating', False)
        mean_restaurant_rating = mean_grouped(df, ['restaurant name','aggregate rating'], 'restaurant name', 'aggregate rating', False)
        expensive_restaurant = df.loc[:, ['restaurant name','average cost for two (usd)']].groupby('restaurant name').max().reset_index().sort_values(by= 'average cost for two (usd)', ascending = False)
        merged1 = pd.merge(count_restaurant_rating, mean_restaurant_rating, on = 'restaurant name')
        merged2 = pd.merge(merged1, expensive_restaurant, on = 'restaurant name')
        merged2.columns = ['Country','Restaurant Name','Count Rate','Avg Rate', 'Price for two (US$)']
        st.markdown(' ### Quantidade de restaurantes por Pais')
        st.dataframe(merged2, use_container_width= True )

    with col2: 
        count_group =count_grouped(df,['country code','restaurant name'], 'country code','restaurant name',False)
        # st.dataframe(count_group, values = 'restaurant name', names = 'country code')
        fig = px.pie(count_group, values = 'restaurant name', names = 'country code')
        st.markdown(' ### Quantidade de restaurantes por Pais')
        st.plotly_chart(fig, use_container_width= True) 
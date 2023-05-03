import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import folium
from haversine import haversine 
from streamlit_folium import folium_static
import os

df = pd.read_csv(r'C:\Users\guga1\OneDrive\Documentos\repos\zomato_restaurants\dataset\new_dataset.csv')

# Agrupamemnto s/ condição
def count_grouped(df, cols, agrouped, by, ascending):
   
    df_aux = df.loc[:, cols].groupby(agrouped).count()\
                            .sort_values(by = by, ascending = ascending).reset_index()
    df_aux = df_aux[by].max()
    
    return df_aux


def count_grouped_onecondition(df, variable, condition,cols, agrouped, by, ascending):
    df_aux = df.loc[df[variable] == condition, cols].groupby(agrouped)\
                                                    .count()\
                                                    .sort_values(by = by, ascending = ascending)\
                                                    .reset_index()
    df_aux = df_aux[by].max()
    
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
    df_aux = df_aux[by].max()
    
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
st.set_page_config(layout = 'wide')

image_file = os.path.join('pages', 'zomatologo.png')
image = Image.open(image_file)

st.sidebar.image(image, width=240)

st.sidebar.markdown('## Zomato')
st.sidebar.markdown("---")

st.write('# Zomato KPI Dashboard - Pais')

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

precos = st.sidebar.multiselect('Preços:',
                                     precos,
                                     default = precos)


st.sidebar.write("---")


culinarias = st.sidebar.multiselect('Culinária:',
                                     culinaria,
                                     default = ['Italian','Arabian','Cafe'])


st.sidebar.write("---")


# filtro de data 
linhas_selecionadas = df['country code'].isin(pais)
df = df.loc[linhas_selecionadas, :]

# filtro de data 
linhas_selecionadas = df['price category'].isin(precos)
df = df.loc[linhas_selecionadas, :]



# ==============================================================================

# ----- Layout ----- 
with st.container():
    country_maps(df)
    

with st.container():
    st.write("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        restaurants_count = df['restaurant name'].nunique()
        col1.metric('Restaurants',restaurants_count)

    with col2:
        variable = 'has online delivery'
        condition = 1 
        cols = ['country code','has online delivery']
        agrouped = ['country code']
        by = 'has online delivery'
        delivery_online = count_grouped_onecondition(df, variable, condition, cols, agrouped, by, False)
        print(delivery_online)
        col2.metric('Count Delivery', delivery_online)

    with col3:
        variable = 'has table booking'
        condition = 1
        cols = ['country code','has table booking']
        agrouped = ['country code']
        by = 'has table booking'
        booking_restaurants = count_grouped_onecondition(df, variable, condition, cols, agrouped, by, False)
        col3.metric('Booking',booking_restaurants)

    with col4:
        cols = ['aggregate rating','country code']
        agrouped = 'country code'
        by = 'aggregate rating'
        count_rate = count_grouped(df,cols, agrouped, by, False )
        col4.metric('Count Rate',count_rate)

        cols = ['aggregate rating','country code']
        agrouped = 'country code'
        by = 'aggregate rating'
        average_rate = mean_grouped(df,cols, agrouped, by, False )
        col4.metric('Average Rate', average_rate )
    
with st.container():
    col1, col2 = st.columns([1,1])
    with col1: 
        country_cuisines = df.loc[:, ['country code','cuisines']].groupby('country code').nunique().reset_index()
        country_delivery = df.loc[:,['country code','has online delivery']].groupby('country code')['has online delivery'].count().reset_index()
        merged_df = pd.merge(country_cuisines,country_delivery, on = 'country code')
        merged_df = merged_df.sort_values(by = 'has online delivery', ascending = False)
        st.markdown('### Delivery by Contry')
        st.dataframe(merged_df)
    
    with col2: 
        avg_for_two_people = df.loc[:, ['average cost for two (usd)','country code']].groupby('country code').mean()\
                                                                             .sort_values(by = 'average cost for two (usd)', ascending = False)\
                                                                             .round(2).reset_index()
        st.markdown('### Average cost for two people (US$)')
        st.dataframe( avg_for_two_people, use_container_width= True)

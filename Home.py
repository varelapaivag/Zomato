import streamlit as st
import pandas as pd
from PIL import Image




# --- Menu ----
image_file = 'pages\zomatologo.png'
image = Image.open(image_file)

st.sidebar.image(image, width=240)

st.sidebar.markdown('## Zomato')
st.sidebar.markdown("---")

st.write('# Zomato KPI Dashboard ')
with st.container():
    st.markdown(""" 
                Zomato Dashboard foi contruido para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
                
                ### Como utilizar:

                -Pais: 
                    - Visualização geográfica
                    - Entregas
                    - Custo para duas pessoas (US$)
                    
                -Cidade: 
                    - Restaurantes por cidade
                    - Culinária por cidade
                    - Métricas
                    - Metricas de serviço

                -Restaurantes: 
                    - Visualização de Avaliações 
                    - Metricas 
                    - Quantidade



                    """)

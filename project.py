import pandas as pd
import psycopg2
import streamlit as st
from PIL import Image
from nutrients import search_nutrients
from ingredients import search_ingredients
from zori_method import search_cook
from basket import basket
from name import search_name

### 조, 조원 이름 추가

if 'choice_name' not in st.session_state:
    st.session_state['choice_name'] = []

if 'choice_kcal' not in st.session_state:
    st.session_state['choice_kcal'] = []

st.set_page_config(layout='wide', page_title = "FOODPIA",page_icon = ":shark:")
st.markdown('<h1 style="text-align:center;">FOODPIA</h1>',unsafe_allow_html = True)
st.markdown('<h2 style="text-align:center;">Food Recommendation System</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:right;">Jiheon Seok</p>',unsafe_allow_html = True)
st.markdown('<p style="text-align:right;">Sojeong Yeon</p>',unsafe_allow_html = True)
st.markdown('<p style="text-align:right;">Yein Hwang</p>',unsafe_allow_html = True)
st.markdown('<p style="text-align:right;">Sungeun Byun</p>',unsafe_allow_html = True)
st.markdown('<p style="text-align:right;">Yoonseok Lee</p>',unsafe_allow_html = True)


search_option = st.selectbox(
        "Select how do you search",
        ('Search', 'Name', 'Nutrients', 'Cook', 'Ingredients','Basket')
    )

if search_option=='Nutrients':
    search_nutrients()

elif search_option=='Name':
    search_name()

elif search_option=='Cook':
    search_cook()

elif search_option=='Ingredients':
    search_ingredients()

elif search_option=='Basket':
    basket()
        

image = Image.open('food.jpg')
st.image(image)

import pandas as pd
import psycopg2
import streamlit as st
from PIL import Image
from TFIDF import tfidf

def search_name():

    if 'name_df' not in st.session_state:
        st.session_state['name_df'] = pd.DataFrame()
    
    if 'name_recipe_name' not in st.session_state:
        st.session_state['name_recipe_name'] = None

    # 연결 정보 입력
    connection_info = "host=147.47.200.145 dbname=teamdb1 user=team1 password=bkms1130 port=34543"
    # PostgreSQL 연결
    conn = psycopg2.connect(connection_info)

    # page1 - 재료 5개 필터링하여 해당 재료가 들어간 요리 추천해주는 기능 구현

    # Create two columns with different width

    st.markdown(""" <style> .font {font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """, unsafe_allow_html=True)

    
    name = st.text_input('요리명', '')

    order_btn = st.radio('How Order the DataFrame?',('칼로리', '추천'))
    desc_btn = st.radio('ASC or DESC?', ('ASC','DESC'))
    search_btn = st.button('요리 추천받기')

    if search_btn == True:

        sql = f"select c.요리명, 칼로리,c.추천 from cooks c join nutrients n on c.id=n.요리id where c.요리명 like \'%{name}%\' "
        
        sql = sql + f'order by {order_btn} {desc_btn} limit 20'
        st.session_state['name_df'] = pd.read_sql(sql, conn)
    
    if not st.session_state['name_df'].empty:
        st.dataframe(data=st.session_state['name_df'])
        st.session_state['name_recipe_name'] = list(st.session_state['name_df'].loc[:,'요리명'])

    if st.session_state['name_recipe_name']:
        
        recipe_name = st.session_state['name_recipe_name']       
        recipe_btn = st.selectbox(
            'Select Recipe',
            recipe_name
        )

        recipe_sql = f'select r.만드는법,r.만드는법_이미지 from recipes r join cooks c on c.id = r.요리id where c.요리명=\'{recipe_btn}\''
        ingredient_sql = f'select 재료정보 from ingredient i join cooks c on i.요리id = c.id where 요리명 = \'{recipe_btn}\''
        recipe_df = pd.read_sql(recipe_sql, conn)
        ingredient = pd.read_sql(ingredient_sql, conn)
        col3, col4 = st.columns([0.8,0.2])
        for i in range(recipe_df.shape[0]):
            recipe_df.iloc[i,1] = '<img src="' + recipe_df.iloc[i,1] + '"width = "300" >'

        with col3:
            st.write(f'재료 정보 : {ingredient.iloc[0,0]}')
            st.write(recipe_df.to_html(escape = False), unsafe_allow_html = True)

        with col4:
            if st.button('Recommend') == True:
                rcmd_sql = f'update cooks set 추천 = 추천 + 1 where 요리명=\'{recipe_btn}\''
                
                cursor = conn.cursor()

                cursor.execute(rcmd_sql)

                conn.commit()

            if st.button('Choose') == True:
                
                sql = f'select 요리명,칼로리 from nutrients n join cooks c on n.요리id = c.id where 요리명 =\'{recipe_btn}\''
                choice = pd.read_sql(sql, conn)
                st.session_state['choice_name'].append(choice.iloc[0,0])
                st.session_state['choice_kcal'].append(choice.iloc[0,1])
                
            st.write('Other cuisine recommendations according to TF-IDF')

            st.dataframe(tfidf(recipe_btn))

    conn.close()

# Add a header and expander in side bar
#st.sidebar.markdown('<p class="font">Foodpia - Food Recommendation System</p>', unsafe_allow_html=True)
#with st.sidebar.expander("About the 'Foodpia'"):
#    st.write(""" Foodpia는 ~~~~ 추천해주는 시스템입니다. 기능에 대한 설명 추가 """)
#image = Image.open('food.jpg')
#st.sidebar.image(image)

# 해당 요리명을 클릭하면 이미지 나오도록 하는 기능 구현 필요!







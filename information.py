import pandas as pd
import psycopg2
import streamlit as st
from PIL import Image
from TFIDF import tfidf

def information():

    # 연결 정보 입력
    connection_info = "host=147.47.200.145 dbname=teamdb1 user=team1 password=bkms1130 port=34543"
    # PostgreSQL 연결
    conn = psycopg2.connect(connection_info)
    cur = conn.cursor()

    st.markdown(""" <style> .font {font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """, unsafe_allow_html=True)

    st.markdown('<p class="font">요리 정보 입력</p>', unsafe_allow_html=True)
    st.info('요리 정보를 추가해보세요~! \n 추가하고 싶은 요리명을 입력하고, 그 요리에 해당하는 정보를 채워주세요~!')

    # info for cooks table
    st.text('어떤 요리를 추가하고 싶으신가요~?')
    name = st.text_input('요리명', '')
    zori_method = st.selectbox(
        '해당 요리의 조리 방법을 선택해주세요.',
        ('볶기', '찌기', '끓이기','굽기','튀기기', '기타'))
    category = st.selectbox(
        '해당 요리의 요리 종류를 선택해주세요.',
        ('반찬', '밥', '국&찌개','일품','후식', '기타'))

    # info for ingredient table
    st.text('해당 요리의 재료정보를 입력해주세요.')
    ingredients = st.text_input('재료정보', '')    
    
    # info for nutrients table
    st.text('해당 요리의 영양소 정보를 입력해주세요. (숫자만 입력)')
    input1 = st.text_input('칼로리', '')
    input2 = st.text_input('탄수화물', '')
    input3 = st.text_input('단백질', '')
    input4 = st.text_input('지방', '')
    input5 = st.text_input('나트륨', '')

    # info for recipes table
    st.text('해당 요리의 레시피 정보를 입력해주세요. (순서대로 입력)')
    recipe1 = st.text_input('만드는 법 1', '')
    recipe2 = st.text_input('만드는 법 2', '')
    recipe3 = st.text_input('만드는 법 3', '')
    recipe4 = st.text_input('만드는 법 4', '')
    recipe5 = st.text_input('만드는 법 5', '')
    recipe6 = st.text_input('만드는 법 6', '')
    recipe7 = st.text_input('만드는 법 7', '')

    input_btn = st.button('요리 정보 추가하기')

    if input_btn == True:

        cursor = conn.cursor()

        # DB에 정보 추가
        cook_id = 'select max(id) from cooks'
        cur.execute(cook_id)
        cook_id = cur.fetchone()[0]

        sql1 = f'insert into cooks values ( {cook_id}+1, \'{name}\', \'{zori_method}\', \'{category}\', null, 0 )'
        sql2 = f'insert into ingredient values ( {cook_id}+1, \'{ingredients}\')'
        sql3 = f'insert into nutrients values ({cook_id}+1, {input1}, {input2}, {input3}, {input4}, {input5})'
        
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        
        recipe_id = 'select max(id) from recipes'
        cur.execute(recipe_id)
        recipe_id = cur.fetchone()[0]
        
        for recipe in [recipe1, recipe2, recipe3, recipe4, recipe5, recipe6, recipe7]:
            if recipe:
                sql4 = f'insert into recipes values ( {recipe_id}+1, {cook_id}+1, \'{recipe}\', null)'
                cursor.execute(sql4)
                recipe_id+=1
        
        conn.commit()

        st.write('요리 정보가 성공적으로 추가되었습니다!')
        
    conn.close()


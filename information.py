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

    col1, col2 = st.columns( [0.5, 0.5])

    with col1:
        name = st.text_input('요리명(필수)', '')

    with col2:
        name_image = st.text_input('요리사진 링크(선택)','')

    zori_method = st.selectbox(
        '해당 요리의 조리 방법을 선택해주세요.(필수)',
        ('볶기', '찌기', '끓이기','굽기','튀기기', '기타'))
    category = st.selectbox(
        '해당 요리의 요리 종류를 선택해주세요.(필수)',
        ('반찬', '밥', '국&찌개','일품','후식', '기타'))

    # info for ingredient table
    st.text('해당 요리의 재료정보를 입력해주세요.(필수)')
    ingredients = st.text_input('재료정보', '')    
    
    # info for nutrients table
    st.text('해당 요리의 영양소 정보를 입력해주세요. (숫자만 입력, 필수)')
    input1 = st.text_input('칼로리', '')
    input2 = st.text_input('탄수화물', '')
    input3 = st.text_input('단백질', '')
    input4 = st.text_input('지방', '')
    input5 = st.text_input('나트륨', '')

    # info for recipes table
    col3, col4 = st.columns( [0.6, 0.4])

    with col3:
        st.text('해당 요리의 레시피 정보를 입력해주세요. (순서대로 입력, 최소 1개 입력)')
        recipe1 = st.text_input('만드는 법 1', '')
        recipe2 = st.text_input('만드는 법 2', '')
        recipe3 = st.text_input('만드는 법 3', '')
        recipe4 = st.text_input('만드는 법 4', '')
        recipe5 = st.text_input('만드는 법 5', '')
        recipe6 = st.text_input('만드는 법 6', '')
        recipe7 = st.text_input('만드는 법 7', '')

    with col4:
        st.text('해당 요리의 레시피 사진 링크를 입력해주세요. (순서대로 입력, 선택)')
        recipe1_link = st.text_input('만드는 법 1 사진 링크', '')
        recipe2_link = st.text_input('만드는 법 2 사진 링크', '')
        recipe3_link = st.text_input('만드는 법 3 사진 링크', '')
        recipe4_link = st.text_input('만드는 법 4 사진 링크', '')
        recipe5_link = st.text_input('만드는 법 5 사진 링크', '')
        recipe6_link = st.text_input('만드는 법 6 사진 링크', '')
        recipe7_link = st.text_input('만드는 법 7 사진 링크', '')

    input_btn = st.button('요리 정보 추가하기')
    condition = True
    essential = [name, zori_method, category, input1, input2, input3, input4, input5, recipe1]
    selection = [name_image, recipe1_link, recipe2_link, recipe3_link, recipe4_link, recipe5_link, recipe6_link, recipe7_link]

    for ess in essential:
        if ess == '':
            condition = False

    if input_btn == True and condition:

        name_image = name_image if name_image!='' else 'null'
        recipe1_link = recipe1_link if recipe1_link!='' else 'null'
        recipe2_link = recipe2_link if recipe1_link!='' else 'null'
        recipe3_link = recipe3_link if recipe1_link!='' else 'null'
        recipe4_link = recipe4_link if recipe1_link!='' else 'null'
        recipe5_link = recipe5_link if recipe1_link!='' else 'null'
        recipe6_link = recipe6_link if recipe1_link!='' else 'null'
        recipe7_link = recipe7_link if recipe1_link!='' else 'null'

        cursor = conn.cursor()

        # DB에 정보 추가
        cook_id = 'select max(id) from cooks'
        cur.execute(cook_id)
        cook_id = cur.fetchone()[0]

        sql1 = f'insert into cooks values ( {cook_id}+1, \'{name}\', \'{zori_method}\', \'{category}\', {name_image}, 0 )'
        sql2 = f'insert into ingredient values ( {cook_id}+1, \'{ingredients}\')'
        sql3 = f'insert into nutrients values ({cook_id}+1, {input1}, {input2}, {input3}, {input4}, {input5})'
        
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        
        recipe_id = 'select max(id) from recipes'
        cur.execute(recipe_id)
        recipe_id = cur.fetchone()[0]
        
        for recipe,link in zip([recipe1, recipe2, recipe3, recipe4, recipe5, recipe6, recipe7], [recipe1_link, recipe2_link, recipe3_link, recipe4_link, recipe5_link, recipe6_link, recipe7_link]):
            if recipe and link!='null':
                sql4 = f'insert into recipes values ( {recipe_id}+1, {cook_id}+1, \'{recipe}\', \'{link}\')'
                cursor.execute(sql4)
                recipe_id+=1
            elif recipe and link=='null':
                sql4 = f'insert into recipes values ( {recipe_id}+1, {cook_id}+1, \'{recipe}\', {link})'
                cursor.execute(sql4)
                recipe_id+=1
        
        conn.commit()

        st.write('요리 정보가 성공적으로 추가되었습니다!')
        
    conn.close()


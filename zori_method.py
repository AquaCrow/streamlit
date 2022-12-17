import streamlit as st
import pandas as pd
import psycopg2
from TFIDF import tfidf

def search_cook():

    if 'cook_df' not in st.session_state:
        st.session_state['cook_df'] = pd.DataFrame()

    if 'cook_recipe_name' not in st.session_state:
        st.session_state['cook_recipe_name'] = None


    # 연결정보 입력
    connection_info = "host=147.47.200.145 dbname=teamdb1 user=team1 password=bkms1130 port=34543"
    # PostgreSQL 연결
    conn = psycopg2.connect(connection_info)

    col,_ = st.columns([0.3,0.7])

    with col:

        option = st.selectbox(
        '원하는 조리 방법을 선택해주세요.',
        ('볶기', '찌기', '끓이기','굽기','튀기기'))

    calrories_check = st.checkbox("칼로리")
    # 최대치 가져오기
    query = "select max(칼로리) from nutrients"
    cur = conn.cursor()
    cur.execute(query)
    val_max = cur.fetchone()[0]
    if calrories_check:
        value = st.slider('당신이 원하는 칼로리의 범위를 설정해주세요.', 0, val_max, (100, 300))
        
        # 확인
        st.write('칼로리 설정: ', value[0], value[1])

    order_btn = st.radio('How Order the DataFrame?',('칼로리', '추천'))
    desc_btn = st.radio('ASC or DESC?', ('ASC','DESC'))
    search_btn = st.button('요리 추천받기')

    if calrories_check:
        sql = f"select id, 요리명, 조리방법, 칼로리, 추천 from cooks c join nutrients n on c.id=n.요리id where 조리방법=\'{option}\' and 칼로리>={value[0]} and 칼로리<={value[1]} order by {order_btn} {desc_btn} limit 20"
    
    else:
        sql = f"select id, 요리명, 조리방법, 칼로리, 추천 from cooks c join nutrients n on c.id=n.요리id where 조리방법=\'{option}\' order by {order_btn} {desc_btn} limit 20"


    if search_btn==True:
        st.session_state['cook_df'] = pd.read_sql(sql, conn)

    
    if not st.session_state['cook_df'].empty:
        st.dataframe(data = st.session_state['cook_df'])
        st.session_state['cook_recipe_name'] = list(st.session_state['cook_df'].loc[:,'요리명'])


    if st.session_state['cook_recipe_name']:
        
        recipe_name = st.session_state['cook_recipe_name']       
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


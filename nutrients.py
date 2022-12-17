import pandas as pd
import psycopg2
import streamlit as st
from PIL import Image
from TFIDF import tfidf

def search_nutrients():
    if 'nut_df' not in st.session_state:
        st.session_state['nut_df'] = pd.DataFrame()
    
    if 'nut_recipe_name' not in st.session_state:
        st.session_state['nut_recipe_name'] = None

    # 연결 정보 입력

    st.markdown(""" <style> .font {font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """, unsafe_allow_html=True)

    st.markdown('<p class="font">영양정보에 따른 요리 추천</p>', unsafe_allow_html=True)
    
    connection_info = "host=147.47.200.145 dbname=teamdb1 user=team1 password=bkms1130 port=34543"
    # PostgreSQL 연결
    conn = psycopg2.connect(connection_info)

    # nutrients - 영양 성분 및 원하는 첨가량에 따른 요리 추천 기능 구현

    # Create two columns with different width
    
    cur = conn.cursor()
    sql = "c.요리명, n.칼로리 from cooks c join nutrients n on c.id = n.요리id"
    nutrients_option = dict()
    st.markdown(""" <style> .font {font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """, unsafe_allow_html=True)

    st.info('직접 설정하고 싶은 영양정보를 체크하세요.')
    col1, col2 = st.columns( [0.5, 0.5])

    with col1:               

        
        # 1. 칼로리
        calrories_check = st.checkbox("칼로리")
        # 최대치 가져오기
        query = "select max(칼로리) from nutrients"
        cur.execute(query)
        val_max = cur.fetchone()[0]
        if calrories_check:
            value = st.slider('당신이 원하는 칼로리의 범위를 설정해주세요.', 0, val_max, (100, 300))
            nutrients_option['n.칼로리'] = (value[0], value[1])
            # 확인
            st.write('칼로리 설정: ', value[0], value[1])
        
        # 2. 탄수화물
        carbohydrates_check = st.checkbox("탄수화물")
        # 최대치 가져오기
        query = "select max(탄수화물) from nutrients"
        cur.execute(query)
        val_max = cur.fetchone()[0]
        if carbohydrates_check:
            value = st.slider('당신이 원하는 탄수화물 함유량 범위를 설정해주세요.', 0, val_max, (100, 300))
            nutrients_option['n.탄수화물'] = (value[0], value[1])
            # 확인
            st.write('탄수화물 함유량 설정: ', value[0], value[1])
        
        # 3. 단백질
        protein_check = st.checkbox("단백질")
        # 최대치 가져오기
        query = "select max(단백질) from nutrients"
        cur.execute(query)
        val_max = cur.fetchone()[0]
        if protein_check:
            value = st.slider('당신이 원하는 단백질 함유량 범위를 설정해주세요.', 0, val_max, (100, 300))
            nutrients_option['n.단백질'] = (value[0], value[1])
            # 확인
            st.write('단백질 함유량 설정: ', value[0], value[1])

        order_btn = st.radio('How Order the DataFrame?',('칼로리', '추천'))
        desc_btn = st.radio('ASC or DESC?', ('ASC','DESC'))
        search_btn = st.button('Search')

    with col2:
        # 4. 지방
        fat_check = st.checkbox("지방")
        # 최대치 가져오기
        query = "select max(지방) from nutrients"
        cur.execute(query)
        val_max = cur.fetchone()[0]
        if fat_check:
            value = st.slider('당신이 원하는 지방 함유량 범위를 설정해주세요.', 0, val_max, (100, 300))
            nutrients_option['n.지방'] = (value[0], value[1])
            # 확인
            st.write('지방 함유량 설정: ', value[0], value[1])    
            
        # 5. 나트륨
        natrium_check = st.checkbox("나트륨")
        # 최대치 가져오기
        query = "select max(나트륨) from nutrients"
        cur.execute(query)
        val_max = cur.fetchone()[0]
        if natrium_check:
            value = st.slider('당신이 원하는 나트륨 함유량 범위를 설정해주세요.', 0, val_max, (100, 300))
            nutrients_option['n.나트륨'] = (value[0], value[1])
            # 확인
            st.write('지방 함유량 설정: ', value[0], value[1])    
        
    
    if search_btn == True:
        # default sql 
        sql_select = "select c.요리명, n.칼로리"
        sql_join = " from cooks c join nutrients n on c.id = n.요리id"
        sql_where = ""
        
        if nutrients_option:
            for k, v in nutrients_option.items():
                if k != 'n.칼로리':
                    sql_select = sql_select + ', ' + k
                    
                sql_where = sql_where + f" and ({k} between {v[0]} and {v[1]})"
                
        sql_select = sql_select + ', ' + 'c.추천'
    
        sql = sql_select + sql_join + sql_where + f' order by {order_btn} {desc_btn} limit 20'
        st.session_state['nut_df'] = pd.read_sql(sql, conn)
            
    if (st.session_state['nut_df'].empty):
        st.info("아쉽게도 원하는 영양 성분이 담긴 요리가 없네요.ㅠ 조건을 바꿔서 다시 검색해보세요!")
        st.session_state['nut_recipe_name'] = None

    else:
        st.info('당신이 원하는 영양 성분이 담긴 요리 리스트를 확인해보세요.')
        st.dataframe(data = st.session_state['nut_df'])
        st.session_state['nut_recipe_name'] = list(st.session_state['nut_df'].loc[:, '요리명'])
    
    if st.session_state['nut_recipe_name']:
        
        recipe_name = st.session_state['nut_recipe_name']       
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
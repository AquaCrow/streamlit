import pandas as pd
import psycopg2
import streamlit as st
from PIL import Image
from TFIDF import tfidf

def search_ingredients():

    if 'ing_df' not in st.session_state:
        st.session_state['ing_df'] = pd.DataFrame()
    
    if 'ing_recipe_name' not in st.session_state:
        st.session_state['ing_recipe_name'] = None

    # 연결 정보 입력
    connection_info = "host=147.47.200.145 dbname=teamdb1 user=team1 password=bkms1130 port=34543"
    # PostgreSQL 연결
    conn = psycopg2.connect(connection_info)

    # page1 - 재료 5개 필터링하여 해당 재료가 들어간 요리 추천해주는 기능 구현

    # Create two columns with different width

    st.markdown(""" <style> .font {font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """, unsafe_allow_html=True)

    st.markdown('<p class="font">원하는 재료를 활용한 요리 추천</p>', unsafe_allow_html=True)
    st.info('냉장고 재고를 털어보아요~! \n 요리에 활용하고 싶은 재료 5개를 넣어주세요. 앞 칸부터 순차적으로 적어주세요. (최소 1개/ 최대 5개)')
    col1, col2 = st.columns( [0.5, 0.5])
    with col1:               

        input1 = st.text_input('재료1', '')
        input3 = st.text_input('재료3', '')
        input5 = st.text_input('재료5', '')

    
    with col2:
        input2 = st.text_input('재료2', '')
        input4 = st.text_input('재료4', '')
        inputs = [input2, input3, input4, input5]

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

    if search_btn == True:

        st.write('위 재료들을 활용한 요리 추천리스트~!')
        inputs = [input2, input3, input4, input5]
        
        sql = f"select c.요리명, 칼로리,c.추천, 재료정보 from ingredient i join cooks c join nutrients n on c.id=n.요리id on c.id = i.요리id where i.재료정보 like \'%{input1}%\' "
        for i in inputs:
            if i == '':
                break
            sql = sql + 'and '
            sql = sql + f"i.재료정보 like \'%{i}%\' "
        
        if calrories_check:
            sql = sql + f'and 칼로리>={value[0]} and 칼로리<={value[1]}'
        sql = sql + f'order by {order_btn} {desc_btn} limit 20'
        st.session_state['ing_df'] = pd.read_sql(sql, conn)
    
    if not st.session_state['ing_df'].empty:
        st.dataframe(data=st.session_state['ing_df'])
        st.session_state['ing_recipe_name'] = list(st.session_state['ing_df'].loc[:,'요리명'])

    if st.session_state['ing_recipe_name']:
        
        recipe_name = st.session_state['ing_recipe_name']       
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
            if recipe_df.iloc[i,1]:
                recipe_df.iloc[i,1] = '<img src="' + recipe_df.iloc[i,1] + '"width = "300" >'

        with col3:
            st.write(f'재료 정보 : {ingredient.iloc[0,0]}')
            st.write(recipe_df.to_html(escape = False), unsafe_allow_html = True)

        with col4:
            recommend_btn = st.button('Recommend')
            choose_btn = st.button('Choose')

            st.write('Other cuisine recommendations according to TF-IDF')

            st.dataframe(tfidf(recipe_btn))

            if recommend_btn== True:
                rcmd_sql = f'update cooks set 추천 = 추천 + 1 where 요리명=\'{recipe_btn}\''
                
                cursor = conn.cursor()

                cursor.execute(rcmd_sql)

                conn.commit()

            if choose_btn == True:
                
                sql = f'select 요리명,칼로리 from nutrients n join cooks c on n.요리id = c.id where 요리명 =\'{recipe_btn}\''
                choice = pd.read_sql(sql, conn)
                st.session_state['choice_name'].append(choice.iloc[0,0])
                st.session_state['choice_kcal'].append(choice.iloc[0,1])
                
        
    conn.close()

# Add a header and expander in side bar
#st.sidebar.markdown('<p class="font">Foodpia - Food Recommendation System</p>', unsafe_allow_html=True)
#with st.sidebar.expander("About the 'Foodpia'"):
#    st.write(""" Foodpia는 ~~~~ 추천해주는 시스템입니다. 기능에 대한 설명 추가 """)
#image = Image.open('food.jpg')
#st.sidebar.image(image)

# 해당 요리명을 클릭하면 이미지 나오도록 하는 기능 구현 필요!







import pandas as pd
import psycopg2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def tfidf(name):

    # 연결 정보 입력
    connection_info = "host=147.47.200.145 dbname=teamdb1 user=team1 password=bkms1130 port=34543"
    # PostgreSQL 연결
    conn = psycopg2.connect(connection_info)

    sql1 = "select 재료정보 from ingredient i"
    sql2 =f"select 재료정보 from ingredient i join cooks c on c.id = i.요리id where c.요리명 = '{name}'"
    sql_name = "select 요리명 from cooks c"

    total = list(pd.read_sql(sql1, conn)['재료정보'])
    obj = list(pd.read_sql(sql2, conn)['재료정보'])
    recipe = np.array(pd.read_sql(sql_name, conn)['요리명'])
    conn.close()

    vect = TfidfVectorizer()
    tfvect = vect.fit(total)

    tfidv_df = pd.DataFrame(tfvect.transform(total).toarray())
    obj_df = pd.DataFrame(tfvect.transform(obj).toarray())

    sim = cosine_similarity(obj_df, tfidv_df)
    
    idxs = list(sim.argsort().squeeze(0)[1:6])

    return pd.DataFrame(recipe[idxs], columns = ['요리명'])
        
    

# Add a header and expander in side bar
#st.sidebar.markdown('<p class="font">Foodpia - Food Recommendation System</p>', unsafe_allow_html=True)
#with st.sidebar.expander("About the 'Foodpia'"):
#    st.write(""" Foodpia는 ~~~~ 추천해주는 시스템입니다. 기능에 대한 설명 추가 """)
#image = Image.open('food.jpg')
#st.sidebar.image(image)

# 해당 요리명을 클릭하면 이미지 나오도록 하는 기능 구현 필요!







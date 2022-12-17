import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import psycopg2

def basket():

    gender = st.radio("What's gender?",('Male', 'Female'))

    if gender == 'Male':
        total = 900
    else:
        total = 700
    
    names = st.session_state['choice_name']
    kcals = st.session_state['choice_kcal']

    if names == []:
        st.subheader("You don't choose any food")
    
    else:
        st.subheader(f"한 끼 적정 칼로리 : {total}")
        st.subheader(f"선택한 칼로리 : {sum(kcals)}")

        remain = total - sum(kcals)
        if remain>=0:
            labels = names + ['Nothing']
            values = kcals + [remain]
        
        else:
            st.write("You should eat a little")
            labels = names
            values = kcals
        
        fig = go.Figure(data = [go.Pie(labels = labels, values = values, textinfo='label + percent',
        insidetextorientation = 'radial')])

        st.plotly_chart(fig, use_container_width = True)

        if remain>0:

            connection_info = "host=147.47.200.145 dbname=teamdb1 user=team1 password=bkms1130 port=34543"
    
            conn = psycopg2.connect(connection_info)
            sql = f'select 요리명,칼로리 from nutrients n join cooks c on n.요리id = c.id where 칼로리<={remain} order by 칼로리 desc limit 50'
            remains = pd.read_sql(sql, conn)
            st.dataframe(remains)
            conn.close()
import streamlit as st
from pymongo import MongoClient
import pandas as pd
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

st.write('<h1 style="text-align:center;color :black">Covid-19 Analysis</h1>', unsafe_allow_html=True)
st.write('<h2 style="text-align:center;color :black">using MongoDB</h2>', unsafe_allow_html=True)

client = MongoClient('mongodb://localhost:27017')
db = client['india']
collection = db['covid_india']
user_collection = db['users']


cursor = collection.find({},{'_id':0, "State/UTs":1})
states = []
for record in cursor:
    states.append(record['State/UTs'])



state = st.selectbox('select a state', states)

col1, col2, col3 = st.columns([1,1,1])
with col1:
    active = st.button('Active')
    if active:
        res1 = collection.find({'State/UTs': state}, {'_id':0, 'Active':1})
        val1 = list(res1[0].values())
        p_df = pd.DataFrame([val1], columns=['Active'])

        st.dataframe(p_df)    

with col2:
    p_cases = st.button('total cases')
    if p_cases:
        res2 = collection.find({'State/UTs': state}, {'_id':0, 'Total Cases':1})
        val2 = list(res2[0].values())
        p_df = pd.DataFrame([val2], columns=['Total Cases'])

        st.dataframe(p_df)

with col3:
    deaths = st.button('deaths')
    if deaths:
        res3 = collection.find({'State/UTs': state}, {'_id':0, 'Deaths':1})
        val3 = list(res3[0].values())
        p_df = pd.DataFrame([val3], columns=['Deaths'])

        st.dataframe(p_df)

summary = st.button('show state summary')

if summary:
    db_summary = collection.find({'State/UTs': state}, {'_id':0})

    keys = list(db_summary[0].keys())
    vals = list(db_summary[0].values())

    df = pd.DataFrame([vals],columns=keys)

    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    st.table(df)

st.write('<h2 style="text-align:center;color :white">Data Analysis</h2>', unsafe_allow_html=True)

total_db = collection.find({}, {'_id':0})
keys = list(total_db[0].keys())
vals = list(total_db)
with st.expander('Total Data in json format'):
    st.write(vals)

with st.expander('Total Data in table format'):
    t_df = pd.DataFrame.from_dict(vals)
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(t_df)

with st.expander('total cases'):
    temp = st.radio('Choose',['pie chart', 'bar graph'])
    t_df = pd.DataFrame.from_dict(vals)
    x_axis = t_df['State/UTs']
    y_axis = t_df['Total Cases']
    if temp == 'bar graph':
        
        fig = px.bar(t_df, x="State/UTs", y="Total Cases",width=675, height=650, title="Total Cases as per each State : ")
        st.plotly_chart(fig)
    elif temp == 'pie chart':
        fig = px.pie(t_df, values='Total Cases', names=t_df['State/UTs'].T,title='Covid cases (%) in all states of India')
        st.plotly_chart(fig)

with st.expander('explore India'):
    temp = st.radio('choose',['total cases', 'Deaths'])
    t_df = pd.DataFrame.from_dict(vals)

    if temp == 'total cases':
        fig = px.choropleth(
                    t_df,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State/UTs',
                    color='Total Cases',
                    color_continuous_scale='Reds',
                    projection='mercator',
                    title='Total Cases in India'
                    )
        fig.update_layout(width=650, height=700, autosize=False, margin = dict(l=0,r=0,b=0,t=0,pad=4,autoexpand=True),
geo=dict(bgcolor= 'rgba(0,0,0,0)'))
        fig.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig)
    
    
    elif temp == 'Deaths':
        fig = px.choropleth(
            t_df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State/UTs',
            color='Deaths',
            projection='mercator',
            color_continuous_scale='Blues'
        )
        fig.update_layout(width=650, height=700, autosize=False, margin = dict(l=0,r=0,b=0,t=0,pad=4,autoexpand=True),
geo=dict(bgcolor= 'rgba(0,0,0,0)'))

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        




def retriever(q):
    if q[0] == 'Active':
        if q[1] == '>':
            out =  collection.find({q[0]: {'$gt': int(q[2])}})
            return out
        elif q[1] == '<':
            out =  collection.find({q[0]: {'$lt': int(q[2])}})
            return out
    elif q[0] == 'Discharged':
        if q[1] == '>':
            out = collection.find({q[0]: {'$gt': int(q[2])}})
            return out
        elif q[1] == '<':
            out =  collection.find({q[0]: {'$lt': int(q[2])}})
            return out
    elif q[0] == 'Deaths':
        if q[1] == '>':
            out =  collection.find({q[0]: {'$gt': int(q[2])}})
            return out
        elif q[1] == '<':
            out =  collection.find({q[0]: {'$lt': int(q[2])}})
            return out
    elif q[0] == 'TotalCases':
        if q[1] == '>':
            out =  collection.find({'Total Cases': {'$gt': int(q[2])}})
            return out
        elif q[1] == '<':
            out =  collection.find({'Total Cases': {'$lt': int(q[2])}})
            return out
    elif q[0] == 'ActiveRatio':
        if q[1] == '>':
            out =  collection.find({"Active Ratio (%)": {'$gt': float(q[2])}})
            return out
        elif q[1] == '<':
            out =  collection.find({"Active Ratio (%)" : {'$lt': float(q[2])}})
            return out
    elif q[0] == 'DischargeRatio':
        if q[1] == '>':
            out =  collection.find({"Discharge Ratio (%)": {'$gt': float(q[2])}})
            return out
        elif q[1] == '<':
            out =  collection.find({"Discharge Ratio (%)" : {'$lt': float(q[2])}})
            return out
    elif q[0] == 'DeathRatio':
        if q[1] == '>':
            out =  collection.find({"Death Ratio (%)": {'$gt': float(q[2])}})
            return out
        elif q[1] == '<':
            out =  collection.find({"Death Ratio (%)" : {'$lt': float(q[2])}})
            return out
    




def login_form():
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        return username, password
def signup_form():
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    return username, password

if 'name' not in st.session_state:
    st.session_state.name = ''


def update(username):
    st.session_state.name = username

def your_query(query):
    st.write(query)


with st.expander('Login to write Query !!'):
    # st.write(st.session_state)
    home = st.selectbox('Home', ['sign_up', 'login'])
    if home == 'sign_up':
        username, password = signup_form()
        if st.button('sign_up'):
            if "" in [username, password]:
                st.error('some fields are missing')
            elif user_collection.find_one({'user': username}):
                st.error('user already exist')
            else:
                user_collection.insert_one({'user':username, 'password':password, 'Queries': []})
                st.success('Account created successfully')
                st.info('please move to login page')
    
    elif home == 'login':
        username, password = login_form()
        login = st.button('Login', on_click=update(username))
        if login:
            if "" in [username, password]:
                st.error('some fields are missing')
            elif (user_collection.find_one({'user': username, 'password': password})):
                if st.session_state.name:
                    # st.write(st.session_state)
                    st.success('Login successful!! write your query now')
                    
            elif not user_collection.find_one({'user': username, 'password': password}):
                st.error('username or password is incorrect !!')
            else:
                st.error('password incorrect !!')

with st.expander('Query Form'):
    # st.write(st.session_state)
    st.write(f'Welcome {st.session_state.name} !!')
    # ke = list(collection.find().limit(1))
    li = ['Active', 'Discharged', 'Deaths', 'ActiveRatio', 'DischargeRatio', 'DeathRatio', 'TotalCases']
    st.info(f'write query to know above items {li}')
    query = st.text_input('write query')
    submit = st.button('submit')
    if submit:
        if query == '':
            st.error('Type a valid Query')
        elif st.session_state.name != '':
            if user_collection.find_one({'user':st.session_state.name, 'Queries': query}):
                pass
            else:
                user_collection.update_one({'user':st.session_state.name}, {'$push': {'Queries':query}})
            query = query.split()
            res = retriever(query)
            out = list(res)
            states = [state['State/UTs'] for state in out]
            
            if query[0] == 'ActiveRatio':
                inko = [state['Active Ratio (%)'] for state in out]
            
            elif query[0] == 'DeathRatio':
                inko = [state['Death Ratio (%)'] for state in out]
            
            elif query[0] == 'DischargeRatio':
                inko = [state['Discharge Ratio (%)'] for state in out]
            
            elif query[0] == 'TotalCases':
                inko = [state['Total Cases'] for state in out]
            
            else:
                inko = [state[query[0]] for state in out]
            data = np.array([states, inko])
            df = pd.DataFrame(data.T, columns=['State/UTs',query[0]])
            st.dataframe(df)
        else:
            st.error('please login first')
    if st.session_state.name != '':
        logout = st.button('Logout', on_click=update(''))
        if logout:
            st.success('Logged out successfully')   




# to = collection.aggregate([{'Total cases': {'$sum': {'Total cases'}}}])
# st.write(list(to))

   


    



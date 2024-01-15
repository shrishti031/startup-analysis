import matplotlib.pyplot as plt
#st.set_page_config(layout='wide',page_title='StartUp Analysis')
# st.title('Startup Dashboard')
# st.header('I am learning')
# st.subheader('I am loving it')
# st.write('This is normal text')
# st.markdown("""
# ### My favourite movies
# - Race
# - When you fall inn love
# - Hostages
# """)
import streamlit as st
import pandas as pd
st.set_page_config(layout='wide',page_title='StartUp Analysis')
df = pd.read_csv("startup_cleaned.csv")
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load(inv):
    st.title(inv)
    last=df[df['investors'].str.contains('inv')].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Recent Investments')
    st.dataframe(last)
    col1,col2=st.columns(2)
    with col1:
         big=df[df['investors'].str.contains(' IDG Ventures')].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
         st.subheader('Big Investments')
    #st.dataframe(big)
         fig,ax=plt.subplots()
         ax.bar(big.index, big.values)
         st.pyplot(fig)
    with col2:
        vertical=df[df['investors'].str.contains('inv')].groupby('city')['amount'].sum()
        fig, ax = plt.subplots()
        ax.pie(vertical,labels=vertical.index)
        st.pyplot(fig)
    st.title('Sector wise Investment')
    vertical2 = df[df['investors'].str.contains('inv')].groupby('round')['amount'].sum()
    fig, ax = plt.subplots()
    ax.pie(vertical2, labels=vertical2.index)
    st.pyplot(fig)
    st.title('City wise Investment')
    vertical3 = df[df['investors'].str.contains('inv')].groupby('city')['amount'].sum()
    fig, ax = plt.subplots()
    ax.pie(vertical3, labels=vertical3.index)
    st.pyplot(fig)
    st.title('Year-Wise Investment')
    df['year'] = df['date'].dt.year
    vf4=df[df['investors'].str.contains(' IDG Ventures')].groupby('year')['amount'].sum()
    fig, ax = plt.subplots()
    ax.plot(vf4.index,vf4.values)
    st.pyplot(fig)
def load_overall():
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total', str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.metric('Avg', str(round(avg_funding)) + ' Cr')

    with col4:
        st.metric('Funded Startups', num_startups)
    st.header('MoM graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])


    st.pyplot(fig3)

st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('select one',['Overall Analysis','Startup', 'Investor'])
if option =='Overall Analysis':

        load_overall()

elif option == 'Startup':
    st.sidebar.selectbox('select startup', sorted(df['startup'].unique().tolist()))
    st.title('Startup Analysis')
    btn1 = st.sidebar.button('Find Startup Details')
else:
    inv=st.sidebar.selectbox('select startup',sorted(set(df['investors'].str.split(',').sum())))

    btn2=st.sidebar.button('Investors Details')
    if btn2:
        load(inv)


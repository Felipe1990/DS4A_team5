import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import time
import utils

# sidebar

st.sidebar.markdown("""
                # Model inputs

                ## Loan properties:
                """)

loan_size = st.sidebar.number_input('Loan size', min_value=100, max_value=2000000, step=100, value=200)

st.sidebar.markdown("""
                    ## Characteristics of the property:
                    """)

property_address = st.sidebar.text_input('Property Adress', value='SCN Quadra 02')
property_city = st.sidebar.text_input('Property City', value='Brasilia')


run_button = st.sidebar.button('Get result')
result = st.sidebar.empty()


if run_button:
    result.empty()
    # progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # for i in range(1, 101):
    #     status_text.text("%i%% Complete" % i)
    #     progress_bar.progress(i)
    #     time.sleep(0.02)

    # status_text.empty()
    # progress_bar.empty()

else:
    st.empty()

# main panels

st.write("""
         # Property approval model
        """)

# df = pd.DataFrame(
#     np.random.randn(loan_size, 3),
#     columns=['a', 'b', 'c'])

# c = alt.Chart(df).mark_circle().encode(x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

if run_button:
    
    with st.spinner('Wait for it...'):
        property_location = utils.geo_code(property_address, property_city)
        df = pd.DataFrame({'lat': [np.round(property_location['lat'], 5)],  
                        'lon': [np.round(property_location['lng'], 5)]},
                            index=[0])
        cod_sector = utils.convert_geo_to_sector_code(property_location, {'Distrito Federal': 'df'}, '../data/sharp')
    
    st.map(df, zoom=14)        
    st.write(property_location)
    # st.text(property_location['state_name'])
    st.text(cod_sector)

    if np.random.normal()>0.5:
        st.success('Accepted')
    else: 
        st.info('Rejected')
    
    
    # st.altair_chart(c, use_container_width=True)
else:
    st.empty()



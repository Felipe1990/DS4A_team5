import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import time

# sidebar

st.sidebar.markdown("""
                # Model inputs

                ## Loan properties:
                """)

loan_size = st.sidebar.number_input('Loan size', min_value=100, max_value=2000000, step=100, value=200)

st.sidebar.markdown("""
                    ## Characteristics of the property:
                    """)

property_address = st.sidebar.text_input('Property Adress')

run_button = st.sidebar.button('Get result')
result = st.sidebar.empty()


if run_button:
    result.empty()
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    for i in range(1, 101):
        status_text.text("%i%% Complete" % i)
        progress_bar.progress(i)
        time.sleep(0.02)

    status_text.empty()
    progress_bar.empty()
    
    if np.random.normal()>0.5:
        result.markdown('Accepted')
    else: 
        result.markdown('Rejected')

else:
    st.empty()

# main pane

st.write("""
         # Property approval model
        """)

df = pd.DataFrame(
    np.random.randn(loan_size, 3),
    columns=['a', 'b', 'c'])

c = alt.Chart(df).mark_circle().encode(x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

if run_button:
    st.altair_chart(c, use_container_width=True)
else:
    st.empty()


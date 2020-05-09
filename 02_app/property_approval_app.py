import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import time
import utils
import os 
import pickle
import joblib

###### load model scaler and colnames
# load colnames
filename_colnames = '../data/var_names.pkl'
with open(filename_colnames, 'rb') as f:
    relevant_variables_rf = pickle.load(f)

# save scaler
filename_scaler = '../data/feature_scaler.pkl'
with open(filename_scaler, 'rb') as f:
    final_scaler = pickle.load(f)

# load model
filename_model = '../data/acceptance_model.sav'
loaded_model = joblib.load(filename_model)


################# data get request
url_request = 'https://webhooks.mongodb-stitch.com/api/client/v2.0/app/getinfocensus-fzwgb/service/getCensusInfo/incoming_webhook/webhook0?'
dict_states = {'Distrito Federal': 'df', 'São Paulo':'sp', 'Sao Paulo':'sp'}

# sidebar
st.sidebar.markdown("""
                # Property approval model

                ## Model inputs

                ### Characteristics of the loan:
                """)

loan_size = st.sidebar.number_input('Loan size', min_value=100, max_value=2000000, step=100, value=200)

st.sidebar.markdown("""
                    ### Characteristics of the property:
                    """)

property_address = st.sidebar.text_input('Property Adress', value='R. Itapeva, 636 - Bela Vista')
property_municipality = st.sidebar.selectbox('Property municipality', ['São Paulo'])
property_metropolitan_region = st.sidebar.selectbox('Metropolitan region', ['São Paulo'])

run_button = st.sidebar.button('Get result')
result = st.sidebar.empty()

if run_button:
    result.empty()
    status_text = st.sidebar.empty()

else:
    st.empty()

# main panels

if run_button:
    # t_rex = st.write('<iframe width="560" height="315" src="http://wayou.github.io/t-rex-runner/"></iframe>', unsafe_allow_html=True)
    with st.spinner('Please wait...'):
        property_location = utils.geo_code(property_address, property_municipality+', '+property_metropolitan_region)
        df = pd.DataFrame({'lat': [np.round(property_location['lat'], 5)],  
                        'lon': [np.round(property_location['lng'], 5)]},
                            index=[0])
        cod_sector = utils.convert_geo_to_sector_code(property_location, dict_states, '../data/sharp')

        try:
            df_response = pd.read_json('{0:s}sector={1:s}'.format(url_request, cod_sector), orient='records')
            df_response = df_response.apply(lambda row: row.apply(lambda cell: utils.flat_cell(cell)))

            # scale variables
            features_escaled = df_response.loc[:,relevant_variables_rf]
            features_escaled = pd.DataFrame(final_scaler.transform(features_escaled), columns=features_escaled.columns)

            # make prediction
            model_result = loaded_model.predict(features_escaled)
            # t_rex = st.empty()

        except:
            st.error('Sector nof found in census data')
    
    
    st.map(df, zoom=14)        
    # st.write(property_location)
    # st.text(cod_sector)

    if model_result>0.5:
        st.success('Accepted')
    else: 
        st.info('Rejected')
    
    # st.altair_chart(c, use_container_width=True)
else:
    st.empty()


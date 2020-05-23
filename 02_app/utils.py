import os
import requests
from shapely.geometry import Point
import geopandas as gpd

def geo_code(address, city):
    """
    Geo code address sing open maps API
    
    Parameters
    ------------
    
    address: str
        Address as clear as possible, better to check first if it can be found in open street search engine
    city: str
        Name of the city
        
    Returns
    ---------
    
    results: dict
        dictionary with latitude, longitud and state name information
    
    """
    parameters = {'key': os.environ.get("CON_KEY"),
                  'location': '{0:s}, {1:s}, Brazil'.format(address, city),
                  'thumbMaps': False,
                  'maxResults': 1
                 }
    
    response = requests.get('http://www.mapquestapi.com/geocoding/v1/address', params=parameters)

    assert response.status_code==200, 'Review address or internet connection'
    
    results = response.json()['results'][0]['locations'][0]['latLng']
    results['state_name'] = response.json()['results'][0]['locations'][0]['adminArea3']
    results['street_name'] = response.json()['results'][0]['locations'][0]['street']

    assert results['lat']!=39.78373, 'Review address or internet connection'

    return results 


def convert_geo_to_sector_code(geo_code_output, states_dict, path_to_shapes):
    """
    Conver latitud, longitud and state reference to sector code


    Parameters
    ------------

    geo_code_output: dict
        output of geo_code function
    states_dict: dict
        correspondence of states names
    path_to_shapes: str
        path to folder containing shapes

    Returns
    ---------

    sector code: str
    """

    coordinate_point = Point(geo_code_output['lng'], geo_code_output['lat'])
    
    state_in_response = geo_code_output['state_name']
    state_name = states_dict[state_in_response]
    
    assert state_name in os.listdir(path_to_shapes), 'There is no shape available to reference this address'
    
    file_name = [file for file in os.listdir(path_to_shapes+'/'+state_name) if file.find('.shp')>0][0]
    census_sector = gpd.read_file(path_to_shapes+'/{0:s}/{1:s}'.format(state_name, file_name), encoding='latin1')

    sector_code = census_sector.loc[census_sector.contains(coordinate_point), 'CD_GEOCODI'].values[0]

    return sector_code

def flat_cell(cell):
    """
    flat dictionarys in celss

    """
    if isinstance(cell, dict):
        value_cell = list(cell.values())[0]
        
    else:
        value_cell = cell
    
    return value_cell
import shapefile
from json import dumps
import os

# os.chdir('../data')

# Convert Shapefile to GeoJson
def shp_to_geojson(shp, geo_json, encoding='latin1'):
    # read the shapefile
    reader = shapefile.Reader(shp, encoding=encoding)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
       atr = dict(zip(field_names, sr.record))
       geom = sr.shape.__geo_interface__
       buffer.append(dict(type="Feature", geometry=geom, properties=atr)) 

    # write the GeoJSON file
    with open(geo_json, "w", encoding="utf8") as f:
        f.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
        f.close()
        
        
# list_files_shp = {folder_i: ['sharp/'+folder_i+'/'+file for file in os.listdir('sharp/'+folder_i) if file.find('shp')>0] for folder_i in os.listdir('sharp')}
# list_files_shp

# Alternative using geopandas
# import geopandas as gpd

# census_sector_gpd = gpd.read_file('sharp/sc/42SEE250GC_SIR.shp', encoding='latin1')
# census_sector_gpd.to_file('json_shapes/shape_sc.json', driver='GeoJSON')

# census_sector_gpd.head(2)
tippecanoe contratos.geojson -e tiles/ --maximum-zoom=8
find tiles -type f -exec mv '{}' '{}'.gz \;
gunzip -r tiles/


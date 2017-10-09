const fs = require('fs')

const readJSON = (filename) => JSON.parse(fs.readFileSync(filename, "utf8"))
const writeJSON = (data, filename) => fs.writeFileSync(filename, JSON.stringify(data), "utf8")

const municipios = readJSON('../data/municipios.geojson')
const contratos = readJSON('../data/contratos.json')

municipios.features = municipios.features.map(function (feature) {
  var ine = feature.properties.id_ine
  if (ine in contratos) {
    feature.properties = Object.assign({}, feature.properties, contratos[ine])
  } else {
    var vacios = {
      '2017-10-01': 0
    }
    feature.properties = Object.assign({}, feature.properties, vacios)
  }
  return feature
})

writeJSON(municipios, '../data/contratos.geojson')

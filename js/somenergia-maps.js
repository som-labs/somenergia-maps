var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapboxgl-styles/mapa_municipal.json',
    hash: true,
    center: [-2, 40],
    zoom: 5
});

var nav = new mapboxgl.NavigationControl();
map.addControl(nav, 'top-right');

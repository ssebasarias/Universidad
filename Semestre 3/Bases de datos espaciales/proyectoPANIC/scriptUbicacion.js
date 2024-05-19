function initMap() {
    var ubicacion_actual = {lat: -75.5219022, lng: -75.5197082};
    // Crea un objeto de mapa y lo coloca en el elemento HTML con id "map"
    var map = new google.maps.Map(document.getElementById('map'), {
        center: ubicacion_actual,
        zoom: 15
    });
    
    // Agrega un marcador en la ubicación actual
    var marker = new google.maps.Marker({
        position: ubicacion_actual,
        map: map,
        title: 'Ubicación Actual'
    });
}
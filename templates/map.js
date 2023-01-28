var map;
var service;
var infowindow;

async function initialize() {
    var pyrmont = new google.maps.LatLng(-33.8665433, 151.1956316);

    map = new google.maps.Map(document.getElementById('map'), {
        center: pyrmont,
        zoom: 18
    })

    geocoder = new google.maps.Geocoder(); 
    geocode({ address: "Taj Mall" })
}

function geocode(request) {
    var coords = [];
    geocoder
      .geocode(request)
      .then((result) => {
        const { results } = result;
  
        map.setCenter(results[0].geometry.location);
        coords[0] = results[0].geometry.location.lat();
        coords[1] = results[0].geometry.location.lng();
        console.log(coords)
        marker1 = new google.maps.Marker({
            map,
            draggable: false,
            position: { lat: coords[0], lng: coords[1] },
        });
        
      })
      .catch((e) => {
        alert("Geocode was not successful for the following reason: " + e);
      });
 }

google.maps.event.addDomListener(window, 'load', initialize)
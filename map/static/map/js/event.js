$(document).ready(function() {
    $('.subscribe-button').click(function() {
        var button = $(this);
        var eventInnerId = button.data('event-inner-id') || '';
        var eventApiId = button.data('event-api-id') || '';

        var data = {
            csrfmiddlewaretoken: CSRF_TOKEN,
            user_id: user_id,
            event_inner_id: eventInnerId,
            event_api_id: eventApiId
        };

        $.ajax({
            url: '/toggle_event_subscription/',
            method: 'POST',
            data: data,
            success: function(response) {
                if (response.subscribed) {
                    button.text('Вы подписаны');
                } else {
                    button.text('Подписаться');
                }
            }
        });
    });
});


var myMap;
var timer;

ymaps.ready(init);
function init(){
    myMap = new ymaps.Map("map", {
        center: [56.010171, 92.852648],
        zoom: 17
    });

    myMap.controls.remove('typeSelector');
    myMap.controls.remove('trafficControl');
    myMap.controls.remove('fullscreenControl');
    myMap.controls.remove('rulerControl');
    myMap.controls.remove('searchControl');
    myMap.controls.remove('zoomControl');
    myMap.controls.remove('geolocationControl');
    myMap.controls.add('geolocationControl', {
        float: 'none',
        position: {
            top: '55vh',
            right: '5px'
        }
    });
    myMap.controls.add('zoomControl', {
        size: 'small',
        float: 'none',
        position: {
            top: '45vh',
            right: '5px'
        }
    });
}

$(document).ready(function() {
    ymaps.ready(function() {
        geocode();
    });
});

function geocode() {
    var address = document.getElementById('address').textContent;
    ymaps.geocode(address).then(function(res) {
        var coords = res.geoObjects.get(0).geometry.getCoordinates();
        myMap.geoObjects.removeAll();
        myMap.setCenter(coords);
        myMap.geoObjects.add(new ymaps.Placemark(coords));
    });
}

$(document).ready(function() {
    $("#map").hide();
    $("#toggle-map").click(function() {
        $("#map").slideToggle("slow", function() {
            myMap.container.fitToViewport();
            if ($("#map").is(":visible")) {
                $("#toggle-map").text("Скрыть карту");
            } else {
                $("#toggle-map").text("Показать карту");
            }
        });
    });
});
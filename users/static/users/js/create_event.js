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


function geocode() {
    var address = document.getElementById('address').value;
    ymaps.geocode(address).then(function(res) {
        var coords = res.geoObjects.get(0).geometry.getCoordinates();
        myMap.geoObjects.removeAll();
        myMap.setCenter(coords);
        myMap.geoObjects.add(new ymaps.Placemark(coords));
    });
}
function delayedGeocode() {
    clearTimeout(timer);
    timer = setTimeout(geocode, 2000);
}


$(document).ready(function() {
    flatpickr(".date-picker", {
       enableTime: true,
       dateFormat: "d.m.Y H:i",
    });
});


$(document).ready(function() {
    $('#id_image').change(function(e) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('.create_event-main-img-preview').css('background-image', 'url(' + e.target.result + ')');
            $(".create_event-main-img-label span").text("Изменить изображение");
        }
        reader.readAsDataURL(e.target.files[0]);
    });
});


document.addEventListener('DOMContentLoaded', function(){
    var textarea = document.getElementById('id_description');

    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});


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

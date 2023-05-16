ymaps.ready(init);

function createPlacemark(event) {
    console.log(event.location.split(','))
    return new ymaps.Placemark(
        event.location.split(',').map(parseFloat), {
            event: event
        }, {
            balloonContentLayout: MyBalloonLayout,
            balloonPanelMaxMapArea: 0,
            iconLayout: 'default#image',
            iconImageHref: '/static/map/img/point-icon.png',
            iconImageSize: [24, 24],
            iconImageOffset: [-12, -12]
        }
    );
}

function init() {
  var myMap = new ymaps.Map("map", {
    center: [56.010171, 92.852648],
    zoom: 13,
  }, {
    suppressMapOpenBlock: true,
  });

  MyBalloonLayout = ymaps.templateLayoutFactory.createClass(
    '<div class="card" style="width: 18rem;">' +
        '<div class="card-header">' +
            '<a href="event/{{properties.event.id}}">{{properties.event.title}}</a>' +
        '</div>' +
        '{% if properties.event.image_url %}' +
            '<img src="{{properties.event.image_url}}" class="card-img-top" alt="{{properties.event.title}}">' +
        '{% endif %}' +
        '{% if properties.event.description %}' +
        '<div class="card-body">' +
            '<p class="card-text">{{properties.event.description}}</p>' +
        '</div>' +
        '{% endif %}' +
        '{% if properties.event.date %}' +
        '<div class="card-footer">' +
            '<small class="text-muted">Дата: {{properties.event.date}}</small>' +
        '</div>' +
        '{% endif %}' +
    '</div>',

    );

    myMap.controls.remove('typeSelector');
    myMap.controls.remove('trafficControl');
    myMap.controls.remove('fullscreenControl');
    myMap.controls.remove('rulerControl');
    // myMap.controls.remove('searchControl');
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


  events_json.forEach((event) => {
    if (event.location) {
      const placemark = createPlacemark(event);
      myMap.geoObjects.add(placemark);
    }
  });
}

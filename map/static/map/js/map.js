ymaps.ready(init);
var myMap;

function showInfoBox(event, cluster) {
    var infoBox = document.getElementById('infoBox');
    var geoObject = event.get('target');
    var html = '';
    var geoObjects = cluster ? geoObject.getGeoObjects() : [geoObject];
    html += '<div class="main-info_box-address">' + geoObjects[0].properties.get('event').address + '</div>';
    geoObjects.forEach(function(geoObject) {
        var props = geoObject.properties.get('event');
        html +=
            '<div class="main-info_box-event">' +
                '<div class="main-info_box-event-title">' +
                    '<a href="event/' + props.id + '">' + props.title + '</a>' +
                '</div>';
            if (props.image_url) {
                html +=
                '<div class="main-info_box-event-image">' +
                    '<img src="' + props.image_url + '" alt="">' +
                '</div>';
            }
            if (props.description) {
                html +=
                '<div class="main-info_box-event-description">' +
                    '<p>' + props.description + '</p>' +
                '</div>';
            }
            if (props.date) {
                var date = new Date(props.date);
                var formattedDate = date.toLocaleDateString('ru-RU', {
                    day: 'numeric', month: 'long', year: 'numeric',
                    hour: 'numeric', minute: 'numeric'
                });
                html +=
                '<div class="main-info_box-event-date">' +
                    '<p>' + formattedDate + '</p>' +
                '</div>';
            }
            html += '</div>';
    });

    infoBox.innerHTML = html;

    var svgString = `<svg class="svg-close" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="#000000">
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
        <g id="SVGRepo_iconCarrier"> 
            <defs> 
                <style>
                    .c{fill:none;stroke:#131317ff;stroke-linecap:round;stroke-linejoin:round;}
                    .d{fill:#ffdc60;}
                </style> 
            </defs> 
            <g id="a"></g> 
            <g id="b"> 
                <circle class="d" cx="12" cy="12" r="10.5"></circle> 
                <line class="c" x1="6.75" x2="17.25" y1="6.75" y2="17.25"></line> 
                <line class="c" x1="17.25" x2="6.75" y1="6.75" y2="17.25"></line> 
            </g> 
        </g>
    </svg>`;

    var closeButton = document.createElement('div');
    closeButton.innerHTML = svgString;
    closeButton.classList.add("close-button");
    closeButton.addEventListener('click', function() {
        document.querySelector('.main-info_box').style.display = 'none';
    });
    infoBox.appendChild(closeButton);

    document.querySelector('.main-info_box').style.display = 'block';
    setTimeout(updateHeight, 100);
}

function createPlacemark(event) {
    var placemark = new ymaps.Placemark(
        event.location.split(',').map(parseFloat),
        {
            event: event
        },
        {
            iconLayout: ymaps.templateLayoutFactory.createClass('<div class="cluster-layout"></div>'),
            iconShape: {
                type: 'Circle',
                coordinates: [16, 16],
                radius: 16
            }
        }
    );

    placemark.events.add('click', function(e) {
        showInfoBox(e, false);
        var coords = e.get('target').geometry.getCoordinates();
        myMap.panTo(coords, {duration: 1000});
    });

    return placemark;
}

function createClusterLayout() {
    return ymaps.templateLayoutFactory.createClass(
        '<div class="cluster-layout">' +
            '<span class="cluster-number">{{ properties.geoObjects.length }}</span>' +
        '</div>'
    );
}


function init() {
    myMap = new ymaps.Map("map", {
        center: [56.010171, 92.852648],
        zoom: 13,
    }, {
        suppressMapOpenBlock: true,
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

    var clusterer = new ymaps.Clusterer({
        preset: 'islands#invertedVioletClusterIcons',
        groupByCoordinates: true,
        clusterDisableClickZoom: true,
        geoObjectHideIconOnBalloonOpen: false,
        clusterHideIconOnBalloonOpen: false,
        clusterOpenBalloonOnClick: false,
        clusterBalloonPagerSize: 5,
        clusterIconLayout: createClusterLayout(),
        clusterIconShape: {
            type: 'Circle',
            coordinates: [16, 16],
            radius: 16
        }
    });

    clusterer.events.add('click', function(e) {
        showInfoBox(e, true);
        var coords = e.get('target').geometry.getCoordinates();
        myMap.panTo(coords, {duration: 1000});
    });

    events_json.forEach((event) => {
        if (event.location) {
            const placemark = createPlacemark(event);
            clusterer.add(placemark);
        }
    });

    myMap.geoObjects.add(clusterer);
}

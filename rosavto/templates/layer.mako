<%inherit file="master.mako"/>

<%block name="title">Карта + слой</%block>

<div id="map"></div>

<pre>
    Код для добавления слоев заправок и мостов, а также тайлового слоя OpenStreetMap:
    <code data-language="javascript">
        // Загружаем модуль <a href="${request.static_url('rosavto:static/js/rosavto/Map.js')}">rosavto/Map</a> после
        готовности DOM дерева
        require(['rosavto/Map', 'dojo/domReady!'], function (Map) {
        var map = new Map('map', {
        center: [55.7501, 37.6687], // Задаем центр
        zoom: 10 // Указываем начальный зум
        zoomControl: true, // Показываем элемент управления зумом
        legend: true // Показываем легенду карты
        });

        // Добавляем слой с заправками
        map.createGeoJsonLayer('Заправки', '/gas_stations', {color:'#FF0000', opacity: 0.9 });

        // Добавляем слой с мостами
        map.createGeoJsonLayer('Мосты', '/bridges', {opacity:0.9, weight: 2});
        });
    </code>
</pre>

<%block name="inlineScripts">
    <script>
        require([
                    'rosavto/Map', // Модуль карты
                    'rosavto/Layers/MarkersStateClusterLayer', // Слой кластеров
                    'rosavto/NgwServiceFacade',
                    'rosavto/LayersInfo',
                    'dojo/query',
                    'dojo/domReady!'],
                function (Map, MarkersStateClusterLayer, NgwServiceFacade, LayersInfo, query) {
                    var ngwServiceFacade = new NgwServiceFacade(ngwProxyUrl),
                            map = new Map('map', {
                                center: [55.7501, 37.6687],
                                zoom: 10,
                                zoomControl: true,
                                legend: true,
                                easyPrint: false
                            }),
                            layersInfo;

                    map.showLoader();
                    layersInfo = new LayersInfo(ngwServiceFacade);
                    layersInfo.fillLayersInfo().then(function (store) {
                        map.addBaseLayers(layersInfo.getBaseLayers());
                        map.hideLoader();

                        map.createGeoJsonLayer('Заправки', '/gas_stations', {color: '#FF0000', opacity: 0.9 });
                        map.createGeoJsonLayer('Мосты', '/bridges', {opacity: 0.9, weight: 2});
                    });
                });
    </script>
</%block>
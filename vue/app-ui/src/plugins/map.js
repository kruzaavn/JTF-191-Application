import L from 'leaflet'
import ms from "milsymbol";


export default class Map {
    constructor(container_id) {
        let defaults = {
            tile_provider: {
                light: 'https://maps.heigit.org/openmapsurfer/tiles/roads/webmercator/{z}/{x}/{y}.png',
                dark: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
                topographic: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
                imagery: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
            },
            tile_options: {
                attribution: 'Map tiles  <a href="https://leaflet-extras.github.io/leaflet-providers/preview/">attribution</a>',
	            minZoom: 4,
	            maxZoom: 18,
            },
            theme: 'imagery'
        };



        this.container_id = container_id;
        this.map = L.map(this.container_id).setView([0,0], 0);
        L.tileLayer(defaults.tile_provider[defaults.theme], defaults.tile_options).addTo(this.map);
        this.focused = false;
        this.marker_layer = L.featureGroup().addTo(this.map);
        this.map.on('click', this.onClick)
    }

    update_icons(objects) {


        this.marker_layer.clearLayers();

        for (let object in objects) {
            this.plot_icons(objects[object])
        }

        if (!this.focused) {

            this.focus()

        }

        if (this.focused && this.marker_layer.getBounds().getCenter().distanceTo(this.map.getCenter()) > 1000 * 1500.0) {
            this.focused = false
        }
    }

    plot_icons(object) {

        let options = {
                size:20,
                altitudeDepth: Math.round(object.states.LatLongAlt.Alt * 3.28084 / 10) *10,
                additionalInformation: object.states.Name,

            };


            if (object.states.Velocity > 0) {
                options.direction = object.states.Heading * (180/Math.PI);
                options.speed = object.states.Velocity;

            }

        let symbol = new ms.Symbol(icon_dict[object.states.Type['level1']][object.states.CoalitionID],
                                   options
            );

        let icon = L.divIcon({
            className: '',
            html: symbol.asSVG(),
            iconAnchor: new L.Point(symbol.getAnchor().x, symbol.getAnchor().y)
          });

        L.marker([object.states.LatLongAlt.Lat, object.states.LatLongAlt.Long], { icon: icon }).addTo(this.marker_layer)
    }

    focus(){


        try {

            let bounds = this.marker_layer.getBounds();
            this.map.flyToBounds(bounds, {padding: L.point(20,20)});
            this.focused = true
        } catch (e) {

        }
    }

    center_on_point(latlng) {

        this.map.flyTo(latlng, 12)

    }

    onClick(e) {

        console.log('click')

    }

}

let icon_dict = {
    0:{1: 'SHGPU-------', 2: 'SFGPU-------'},
    1:{1: 'SHAP--------', 2: 'SFAP--------'},
    2:{1: 'SHGPU-------', 2: 'SFGPU-------'},
    3:{1: 'SHSP--------', 2: 'SFSP--------'},
    4:{1: 'SHAPW-------', 2: 'SFAPW-------'},
    5:{1: 'SHGPI-----H-', 2: 'SFGPI-----H-'}, };
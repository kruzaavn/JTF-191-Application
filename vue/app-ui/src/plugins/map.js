import L from 'leaflet'
import ms from "milsymbol";


export default class Map {
    constructor(container_id) {
        let defaults = {
            tile_provider: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
            tile_options: {
                attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	            minZoom: 4,
	            maxZoom: 18,
            }
        };
        this.container_id = container_id;
        this.map = L.map(this.container_id).setView([0,0], 0);
        L.tileLayer(defaults.tile_provider, defaults.tile_options).addTo(this.map)
        this.focused = false;
        this.marker_layer = L.layerGroup().addTo(this.map)
    }

    update_icons(objects) {
        this.marker_layer.clearLayers();

        for (let object in objects) {
            this.plot_icons(objects[object])
        }

        if (!this.focused) {

            this.focus()

        }
    }

    plot_icons(object) {

        let symbol = ms.Symbol('SHAP--------', {size: 10});

        let icon = L.divIcon({
            className: '',
            html: symbol.asSVG(),
            iconAnchor: new L.Point(symbol.getAnchor().x, symbol.getAnchor().y)
          });

        L.marker([object.LatLongAlt.Long, object.LatLongAlt.Long], { icon: icon }).addTo(this.marker_layer)
    }

    focus(){


        this.focused = true;

        this.map.flyTo(this.marker_layer.getBounds().getCenter())

    }

}

import L from 'leaflet'
import ms from 'milsymbol'
import 'leaflet/dist/leaflet.css'

export default class Map {
  constructor(container_id) {
    let defaults = {
      tile_provider: {
        default:
          'https://tile.jawg.io/ca78d3b5-f055-4b15-a618-0d8df2bcb947/{z}/{x}/{y}.png?access-token=uAlt2i4a7SyNzAzOthIeEwFZiz4wBCzNipoARw3ENWHNzssJ12SQeABzhgrvTPml',
      },
      tile_options: {
        attribution:
          '<a href=\\"https://www.jawg.io\\" target=\\"_blank\\">&copy; Jawg</a> - <a href=\\"https://www.openstreetmap.org\\" target=\\"_blank\\">&copy; OpenStreetMap</a>&nbsp;contributors',
        minZoom: 4,
        maxZoom: 18,
      },
      theme: 'default',
    }

    this.container_id = container_id
    this.map = L.map(this.container_id).setView([0, 0], 0)
    L.tileLayer(
      defaults.tile_provider[defaults.theme],
      defaults.tile_options
    ).addTo(this.map)
    this.focused = false
    this.marker_layer = L.featureGroup().addTo(this.map)
  }

  remove() {
    this.map.remove()
  }

  update_icons(objects) {
    this.marker_layer.clearLayers()

    objects.forEach((obj) => this.plot_icons(obj))

    if (!this.focused) {
      this.focus()
    }

    if (
      this.focused &&
      this.marker_layer
        .getBounds()
        .getCenter()
        .distanceTo(this.map.getCenter()) >
        1000 * 1500.0
    ) {
      this.focused = false
    }
  }

  plot_icons(object) {
    let options = {
      size: 20,
      altitudeDepth:
        Math.round((object.state.LatLongAlt.Alt * 3.28084) / 10) * 10,
      additionalInformation: object.state.Name,
      infoBackground: 'white',
      direction: object.state.Heading * (180 / Math.PI),
    }

    let symbol = new ms.Symbol(
      icon_dict[object.state.Type['level1']][object.state.CoalitionID],
      options
    )

    let icon = L.divIcon({
      className: '',
      html: symbol.asSVG(),
      iconAnchor: new L.Point(symbol.getAnchor().x, symbol.getAnchor().y),
    })

    L.marker([object.state.LatLongAlt.Lat, object.state.LatLongAlt.Long], {
      icon: icon,
    }).addTo(this.marker_layer)
  }

  focus() {
    try {
      let bounds = this.marker_layer.getBounds()
      this.map.flyToBounds(bounds, { padding: L.point(20, 20) })
      this.focused = true
    } catch (e) {
      console.log(e)
    }
  }

  center_on_point(latlng) {
    this.map.flyTo(latlng, 12)
  }

  onClick() {
    console.log('click')
  }
}

let icon_dict = {
  0: { 1: 'SHGPU-------', 2: 'SFGPU-------' },
  1: { 1: 'SHAP--------', 2: 'SFAP--------' },
  2: { 1: 'SHGPU-------', 2: 'SFGPU-------' },
  3: { 1: 'SHSP--------', 2: 'SFSP--------' },
  4: { 1: 'SHAPW-------', 2: 'SFAPW-------' },
  5: { 1: 'SHGPI-----H-', 2: 'SFGPI-----H-' },
}

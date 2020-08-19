<template>
  <v-container>
    <v-row v-show="!selectedServer" align-content="start">
      <v-card flat>
        <v-card-title>Available Servers</v-card-title>
        <v-row>
          <v-col v-for="server in servers" :key="server.id">
            <v-card
              hover
              class="mx-auto py-auto"
              v-on:click="createMap(server)"
            >
              <v-card-title>{{ server.name }}</v-card-title>
              <v-card-text>
                {{ server.connection_time | dateFormat }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card>
    </v-row>
    <v-row>
      <v-col>
        <v-toolbar flat v-if="selectedServer">
          <v-app-bar-nav-icon></v-app-bar-nav-icon> {{ selectedServer.name }}
          <v-spacer></v-spacer>
          <v-btn outlined tile @click="disconnectSocket" color="error"
            >X</v-btn
          ></v-toolbar
        >
        <div id="map"></div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import map from '@/plugins/map'

export default {
  name: 'GCI',
  data: () => ({
    selectedServer: null,
    map: null,
    units: {
      time: null,
      buffer: [],
      show: [],
    },
    socket: null,
  }),
  methods: {
    ...mapActions(['getServers']),
    configureSocketConnection: function (server) {
      if (window.location.hostname === 'localhost') {
        return `ws://${window.location.hostname}:8000/ws/gci/${server.name}/`
      } else {
        return `wss://${window.location.hostname}/ws/gci/${server.name}/`
      }
    },
    onSocketMessage: function (event) {
      let data = JSON.parse(event.data).message
      let time = data.time
      let state = data.state

      this.units.buffer.push(state)

      if (this.units.time !== time) {
        this.units.time = time
        this.units.show = this.units.buffer
        this.units.buffer = []
        this.units.buffer.push(state)
        this.map.update_icons(this.units.show)
      } else {
        this.units.buffer.push(state)
      }
    },
    disconnectSocket: function () {
      this.units = {
        time: null,
        buffer: [],
        show: [],
      }

      if (this.socket) {
        this.socket.close()
      }

      if (this.map) {
        this.map.remove()
      }
      this.getServers()
      this.socket = null
      this.map = null
      this.selectedServer = null
    },
    createMap: function (server) {
      this.map = new map('map')
      this.selectedServer = server
      this.socket = new WebSocket(this.configureSocketConnection(server))
      this.socket.onmessage = this.onSocketMessage
    },
  },
  computed: {
    ...mapGetters(['servers']),
  },
  filters: {
    dateFormat: function (value) {
      let date = new Date(value)
      return `${date.toLocaleString()}`
    },
  },
  mounted() {
    this.getServers()
  },
  destroyed() {
    this.disconnectSocket()
  },
}
</script>

<style scoped>
#map {
  height: 1000px;
  background-color: rgba(255, 0, 0, 0);
}
</style>

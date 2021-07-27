<template>
  <v-container>
    <v-row v-show="!selectedServer" align-content="start">
      <v-container>
        <v-row>
          <h1>Available Servers</h1>
        </v-row>
        <v-row>
          <v-col
            v-for="server in servers"
            :key="server.id"
            md="4"
            lg="3"
            sm="12"
            class="d-flex child-flex"
          >
            <v-card
              dark
              color="grey"
              class="mx-auto"
              tile
              v-on:click="createMap(server)"
            >
              <v-img
                :src="getTheatreImage(server.theatre)"
                lazy-src="https://jtf191blobstorage.blob.core.windows.net/media/servers/Default.png"
                height="30vh"
                class="my-1"
              >
              </v-img>
              <div class="server-description">
                <v-card-title>Server {{ server.name }}</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-row>
                    <v-col>
                      Mission <v-spacer></v-spacer> Map
                      <v-spacer></v-spacer> Password <v-spacer></v-spacer>
                      Mission Start Time
                    </v-col>
                    <v-col>
                      {{ server.mission }}<v-spacer></v-spacer>
                      {{ server.theatre }}<v-spacer></v-spacer>
                      {{ server.password }}<v-spacer></v-spacer>
                      {{ server.start_time | utcFormat }}
                    </v-col>
                  </v-row>
                </v-card-text>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-row>
    <v-row>
      <v-col>
        <v-toolbar flat v-if="selectedServer">
          <h1>{{ selectedServer.name }}</h1>
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
    socket: null,
  }),
  methods: {
    ...mapActions(['getServers']),
    configureSocketConnection: function (server) {
      if (window.location.hostname === 'localhost') {
        return `ws://${window.location.hostname}:8000/ws/gci/${server.name.replaceAll(' ', '_')}/`
      } else {
        return `wss://${window.location.hostname}/ws/gci/${server.name.replaceAll(' ', '_')}/`
      }
    },
    onSocketMessage: function (event) {
      let data = JSON.parse(event.data).message
      this.map.update_icons(data)
    },
    disconnectSocket: function () {
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
    getTheatreImage: function (theatre) {
      return `https://jtf191blobstorage.blob.core.windows.net/media/servers/${theatre}.png`
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
    utcFormat: function (value) {
      let date = new Date(value)
      return `${date.toString()}`
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
  height: 80vh;
  background-color: rgba(255, 0, 0, 0);
}

.server-description {
  background-color: darkgray;
}
</style>

<template>
  <v-container style="height: 100vh">
    <div v-show="!selectedServer" align-content="start">
      <v-row>
        <v-col>
          <h1>Available Servers</h1>
        </v-col>
      </v-row>
      <v-row>
        <v-col
          v-for="server in servers"
          :key="server.id"
          md="6"
          lg="4"
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
            <div class="description-card">
              <v-card-title>{{ server.name }}</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-row>
                  <v-col>
                    Mission
                    <span class="float-right">{{ server.mission }}</span
                    ><v-spacer></v-spacer> Map
                    <span class="float-right">{{ server.theatre }}</span
                    ><v-spacer></v-spacer> Password
                    <span class="float-right">{{ server.password }}</span
                    ><v-spacer></v-spacer> Start Time
                    <span class="float-right">{{
                      utcFormat(server.start_time)
                    }}</span
                    ><v-spacer></v-spacer> Connection Time
                    <span class="float-right">{{
                      dateFormat(server.connection_time)
                    }}</span
                    ><v-spacer></v-spacer>
                  </v-col>
                </v-row>
              </v-card-text>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>
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
import { mapActions, mapGetters } from "vuex";
import map from "@/plugins/map";

export default {
  name: "GCI",
  data: () => ({
    selectedServer: null,
    map: null,
    socket: null,
  }),
  methods: {
    ...mapActions(["getServers"]),
    configureSocketConnection: function (server) {
      if (window.location.hostname === "localhost") {
        return `ws://${
          window.location.hostname
        }:8000/ws/gci/${server.name.replaceAll(" ", "_")}/`;
      } else {
        return `wss://${
          window.location.hostname
        }/ws/gci/${server.name.replaceAll(" ", "_")}/`;
      }
    },
    onSocketMessage: function (event) {
      let data = JSON.parse(event.data).message;
      this.map.update_icons(data);
    },
    disconnectSocket: function () {
      if (this.socket) {
        this.socket.close();
      }

      if (this.map) {
        this.map.remove();
      }
      this.getServers();
      this.socket = null;
      this.map = null;
      this.selectedServer = null;
    },
    createMap: function (server) {
      this.map = new map("map");
      this.selectedServer = server;
      this.socket = new WebSocket(this.configureSocketConnection(server));
      this.socket.onmessage = this.onSocketMessage;
    },
    getTheatreImage: function (theatre) {
      return `https://jtf191blobstorage.blob.core.windows.net/media/servers/${theatre}.png`;
    },
  },
  computed: {
    ...mapGetters(["servers"]),
    dateFormat: function (value) {
      let date = new Date(value);
      return `${date.toLocaleString("en-US")}`;
    },
    utcFormat: function (value) {
      let date = new Date(value);
      return `${date.toLocaleString("en-US", {
        timeZone: "America/New_York",
      })}`;
    },
  },
  mounted() {
    this.getServers();
  },
  unmounted() {
    this.disconnectSocket();
  },
};
</script>

<style scoped>
#map {
  height: 80vh;
  background-color: rgba(255, 0, 0, 0);
}
</style>

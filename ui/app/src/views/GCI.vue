<template>
  <v-container>
    <h1>server list</h1>
    <v-row row>
      <v-col v-for="server in servers" :key="server.id">
        <v-card hover class="mx-auto" max-width="300">
          <v-card-title>{{ server.name }}</v-card-title>
          <v-card-text>
            {{ server.connection_time }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex'

  export default {
  name: 'GCI',
  methods: {
    ...mapActions(['getServers']),
  },
  computed: {
    ...mapGetters(['servers']),
  },
  mounted() {
    this.getServers()
  },
}
</script>

<style scoped></style>

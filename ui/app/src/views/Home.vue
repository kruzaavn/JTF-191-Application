<template>
    <v-container>
        <h1>Site under construction</h1>
        <h2>{{local}}</h2>
    </v-container>
</template>

<script>
// @ is an alias to /src

import { mapState, mapActions } from 'vuex'

export default {
  name: 'Home',
  components: {
  },
    data: () => ({
      local: location.host,
    }),
  methods: {
      ...mapActions([]),

  },
  computed: {
      ...mapState([]),

  }
}
</script>

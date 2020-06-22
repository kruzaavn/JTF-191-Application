<template>
    <v-container>
        <h1>Site under construction</h1>
    </v-container>
</template>

<script>
// @ is an alias to /src

import { mapState, mapActions } from 'vuex'

export default {
  name: 'Home',
  components: {
  },
  methods: {
      ...mapActions(['increment'])
  },
  computed: {
      ...mapState(['count']),

  }
}
</script>

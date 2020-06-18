<template>
    <v-container>
        <h1>Home Page</h1>
        <p>{{count}}</p>
        <v-btn text v-on:click="increment">increment</v-btn>
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

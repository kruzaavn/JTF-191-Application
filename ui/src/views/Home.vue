<template>
    <v-container>
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

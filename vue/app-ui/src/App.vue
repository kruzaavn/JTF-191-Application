<template>
  <v-app>
    <Banner />

    <v-content>
    <Map />
    </v-content>
  </v-app>
</template>

<script>

import Banner from './components/Banner';
import Map from './components/Map'

export default {
  name: 'App',
  components: {
    Banner,
    Map
  },
  data: () => ({
    //
  }),
};
</script>

<style>
      a {
        text-decoration: none;

    }

    a:hover {
        text-decoration: underline;

    }


</style>
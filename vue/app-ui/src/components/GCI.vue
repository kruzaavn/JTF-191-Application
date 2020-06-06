<template>
  <v-app>
    <Banner />
    <v-content>
    <Map />
    </v-content>
  </v-app>
</template>

<script>
    import Banner from "./atomic_components/Banner";
    import Map from "./atomic_components/Map";

    export default {
        name: "GCI",
        components: {
            Banner,
            Map
        },
    }
</script>

<style scoped>

</style>
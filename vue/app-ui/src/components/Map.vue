<template>
    <v-container id="map" class="map" :fluid="true" :fill-height="true">
    </v-container>
</template>

<script>
    import {mapState} from 'vuex'
    import Map from '../plugins/map.js'
    export default {
        name: "Map",
        computed: mapState({dcs: state => state.dcs.current}),
        data: function () {
            return {
                map: null
                }
            },
        mounted: function () {
            this.initMap()
        },
        methods:  {
            initMap() {

                if (!this.map) {

                    this.map = new Map('map')

                }

            }
        }

    }
</script>

<style scoped>
    .map {

    }

</style>
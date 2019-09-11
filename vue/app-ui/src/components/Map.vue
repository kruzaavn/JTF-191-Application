<template>

    <v-container id="map" class="map" :fluid="true" :fill-height="true">
        <v-card id="roster" class="elevation-1">
            <v-subheader id="header" class="subtitle-2">Active Pilots</v-subheader>
            <v-list>
            <v-list-item v-show="active_pilots" v-bind:onclick="center_on_pilot(pilot)"
                         v-bind:key="key"
                         v-for="(pilot, key) in active_pilots" >{{pilot.states.UnitName}}</v-list-item>
            </v-list>
        </v-card>
    </v-container>
</template>

<script>
    import {mapState, mapGetters} from 'vuex'
    import Map from '../plugins/map.js'
    export default {
        name: "Map",
        computed: {...mapState(['current']),  ...mapGetters(['active_pilots'])},
            // ...mapGetters(['active_pilots'])

        data: function () {
            return {
                map: null,
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
            },

            center_on_pilot(pilot) {

                let latlng = [pilot.states.LatLongAlt.Lat, pilot.states.LatLongAlt.Long];

                this.map.center_on_point(latlng)


            }

        },
        watch: {
            current: function () {
                this.map.update_icons(this.current)
            },
        }

    }
</script>

<style scoped>
    .map{


    }

    #roster{
        position: absolute;
        background: white;
        opacity: .8;
        width: fit-content;
        top: 0vh;
        left: 85vw;
        z-index: 10000;
        margin: 1em;
    }
</style>
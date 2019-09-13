<template>

    <v-container id="map" class="map" :fluid="true" :fill-height="true">
        <v-card v-show="active_pilots" id="roster" class="elevation-1">
            <v-subheader id="header" class="subtitle-2">Active Pilots</v-subheader>
            <v-list>
            <v-list-item class="text-truncate"
                            v-on:click="center_on_pilot(key, current)"
                            v-bind:key="key"
                            v-for="(pilot, key) in active_pilots" >{{pilot}}</v-list-item>
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

            center_on_pilot(key, current) {

                let pilot = current[key];
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
        width: 15vw;
        top: 0vh;
        left: 85vw;
        z-index: 10000;
        margin: 1em;
    }
</style>
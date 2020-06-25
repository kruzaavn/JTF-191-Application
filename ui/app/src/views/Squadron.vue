<template>
    <v-container>
        <v-row align-content="start">
            <v-card
                    tile
            >
                <v-img
                    :src="squadron.img"
                    max-height="400"
                    contain
                >
                    <v-card-title>{{squadronDesignation}}</v-card-title>
                </v-img>

            <v-card
                    class="mx-4 my-5" v-for="member in members"
                    :key="member.id"
                    tile
            >
                <v-row>
                    <v-col
                            cols="2
"
                    >
                <v-img
                        max-height="150"
                        contain
                        :src="'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/' + ranks[member.rank_code] + '.svg'"
                >
                </v-img>
                        </v-col>
                    <v-col>
                <v-card-title>
                    {{member.rank}} {{member.callsign}} {{member.position}}
                </v-card-title>
                <v-card-subtitle>{{member.date_joined}}</v-card-subtitle>
                        </v-col>
                </v-row>
                <v-card-text>
                    <v-row>
                    <v-col>
                    {{member.status}}
                    </v-col>
                    <v-col>
                        {{member.status}}
                    </v-col>
                    </v-row>

                </v-card-text>
            </v-card>
            </v-card>
        </v-row>
    </v-container>
</template>


<script>

    import {mapGetters} from 'vuex'
    export default {
        name: 'Squadron',
        props: ['squadronDesignation'],
        data: () => ({
            ranks: {
        1:'first_lieutenant',
        2: 'second_lieutenant',
        3: 'captain',
        4: 'major',
        5: 'lieutenant_colonel',
        6: 'colonel'}
        }),
        computed: {
            ...mapGetters(['roster', 'squadrons']),
            members:  function (){
                return this.roster.filter(pilot => pilot.squadron.designation === this.squadronDesignation)
            },
            squadron: function () {
                return this.squadrons.filter(sqd => sqd.designation === this.squadronDesignation)[0]
            }
        }

    }
</script>

<style>


</style>
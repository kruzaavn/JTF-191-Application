<template>
    <v-container>
    <h1>some squadron {{squadronDesignation}}</h1>
        <div v-for="member in members" :key="member.id">
            {{member}}
        </div>
    </v-container>
</template>


<script>
    import {mapGetters} from 'vuex'
    export default {
        name: 'Squadron',
        props: ['squadronDesignation'],
        computed: {
            ...mapGetters(['roster']),
            members:  function (){
                return this.roster.filter(pilot => pilot.squadron.designation === this.squadronDesignation)
            }

        }

    }
</script>

<style>


</style>
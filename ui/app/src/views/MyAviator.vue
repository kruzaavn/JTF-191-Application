<template>
    <v-container>
        {{myAviator}}
    </v-container>
</template>


<script>
    import {mapActions, mapGetters} from 'vuex'
    export default {
        name: 'MyAviator',
        computed: {
          ...mapGetters(['myAviator'])
        },
        methods: {
            ...mapActions(['getMyAviator'])
        },
        mounted() {
            this.getMyAviator()
        }
    }
</script>

<style>


</style>
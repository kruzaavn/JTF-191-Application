<template>
    <v-app-bar app>
      <v-toolbar-title class="headline text-uppercase" >
          <a href="https://virtualcvw5.com/">JTF-70</a> Live Server
      </v-toolbar-title>
        <v-spacer></v-spacer>
        <div>Current Server time: {{get_timeString()}}</div>
        <div>| Version: Alpha 0.2</div>
    </v-app-bar>
</template>

<script>
    import {mapState} from 'vuex'
    export default {
        name: "Banner",
        computed: {...mapState(['sim_time']),

        },
        methods: {

            get_timeString: function () {

                let date = new Date(null);
                date.setSeconds(this.sim_time); // specify value for SECONDS here
                return date.toISOString().substr(11, 8);

            }

        }

    }
</script>

<style scoped>

</style>
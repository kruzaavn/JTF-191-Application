<template>
  <v-app id="inspire">
    <v-app-bar
            app
            clipped-right
            color="blue-grey"
            dark
            src="@/assets/logo.svg"
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
          <router-link to="/">
            <v-list-item-content>
              <v-toolbar-title>
                Home
              </v-toolbar-title>
            </v-list-item-content>
          </router-link>
      <v-spacer></v-spacer>
      <Login />
    </v-app-bar>

    <v-navigation-drawer
            v-model="drawer"
            app
    >
      <v-list nav dense>
        <v-list-item>
          <v-list-item-content>
            <router-link tag="ul" to="/about"><v-list-item-title>About Us</v-list-item-title></router-link>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <router-link tag="ul" to="/gci"><v-list-item-title>Web GCI</v-list-item-title></router-link>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <v-container
              class="fill-height"
              fluid
      >
        <v-row
                justify="center"
                align="center"
        >
          <router-view></router-view>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
  import {mapActions} from 'vuex'
  import Login from "./components/Login";
  export default {
    name: "Title",
    components: {Login},
    props: {
      source: String,
    },
    data: () => ({
      drawer: false,
    }),
    methods: {
      ...mapActions(['getRoster', 'getSquadrons', 'getHQs'])
    },
    watch: {
      '$route' (to) {
        document.title = to.meta.title || 'JTF-70'
      }
    },
    mounted() {
      this.getRoster()
      this.getSquadrons()
      this.getHQs()
    }
  }
</script>


<style>
  @import './assets/css/app.css';
</style>
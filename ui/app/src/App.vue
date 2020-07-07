<template>
  <v-app id="inspire">
    <v-app-bar
            app
            clipped-right
            color="#f000000"
            dark

    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <router-link to="/"
            >

            <v-img
                    contain
                    max-width="130px"
                    src="@/assets/logo.png"

                    >
            </v-img>

              </router-link>

      <v-spacer></v-spacer>
      <Login />
    </v-app-bar>

    <v-navigation-drawer
            v-model="drawer"
            app
    >
      <v-list nav dense>
        <v-list-item
                to="/about"
        >
          <v-list-item-content>
            <v-list-item-title>About Us</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item
                to="/gci"
        >
          <v-list-item-content>
            <v-list-item-title>Web GCI</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-group v-for="hq in hqs" :key="hq.id">
          <template v-slot:activator>

            <v-list-item-content>
              <v-list-item-title>{{hq.name}}</v-list-item-title>
            </v-list-item-content>

          </template>

          <v-list-item
                  v-for="subSquadron in squadrons.filter(squadron => squadron.hq && hq.id && squadron.hq.id === hq.id) "
                  :key="subSquadron.id"
                  :to="/squadron/ + subSquadron.designation"
          >
            <v-list-item-content>
            <v-list-item-title>
            {{subSquadron.designation}}
            </v-list-item-title>
              </v-list-item-content>
          </v-list-item>

        </v-list-group>
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
  import {mapActions, mapGetters} from 'vuex'
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
    computed: {
      ...mapGetters(['squadrons','hqs']),
    },
    methods: {
      ...mapActions(['getRoster', 'getSquadrons', 'getHQs']),
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

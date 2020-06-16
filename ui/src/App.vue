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
          <router-link tag="btn" to="/">
            <v-list-item-content>
              <v-toolbar-title>
                Home
              </v-toolbar-title>
            </v-list-item-content>
          </router-link>
      <v-spacer></v-spacer>
      <v-btn class="ma-2" tile outlined color="white">
        <v-icon left>mdi-login</v-icon> login
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer
            v-model="drawer"
            app
    >
      <v-list dense>
        <v-list-item @click.stop="left = !left">
          <v-list-item-content>
            <router-link tag="ul" to="/about"><v-list-item-title>About Us</v-list-item-title></router-link>
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
  export default {
    name: "Title",
    props: {
      source: String,
    },
    data: () => ({
      drawer: false,
    }),
    watch: {
      '$route' (to) {
        document.title = to.meta.title || 'JTF-70'
      }
    },
  }
</script>


<style>
  @import './assets/css/app.css';
</style>
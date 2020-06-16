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
      <v-toolbar-title>
        <router-link to="/">Home</router-link>
      </v-toolbar-title>
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
            <v-list-item-title><router-link to="/about">About Us</router-link></v-list-item-title>
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
  }
</script>


<style>
  @import './assets/css/app.css';
</style>
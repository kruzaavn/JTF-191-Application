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
      <v-toolbar-title>Home</v-toolbar-title>
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
          <v-list-item-action>
            <v-icon>mdi-exit-to-app</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Open Temporary Drawer</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-navigation-drawer
            v-model="left"
            fixed
            temporary
    ></v-navigation-drawer>

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
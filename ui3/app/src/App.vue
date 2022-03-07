<template>
  <v-app id="inspire" :theme="theme">
    <v-app-bar>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <router-link to="/">
        <v-img min-width="150px" max-width="250px" src="@/assets/logo.png">
        </v-img>
      </router-link>
      <v-spacer></v-spacer>

      <v-btn
        v-if="isAdmin"
        color="white"
        outlined
        tile
        depressed
        :href="adminLink"
      >
        ADMIN
      </v-btn>
      <LoginComponent />
      <v-btn @click="toggleTheme">toggle theme</v-btn>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" app>
      <v-list nav dense>
        <v-list-item to="/">
          <v-list-item-title>Photos</v-list-item-title>
        </v-list-item>
        <v-list-item to="/about">
          <v-list-item-title>About Us</v-list-item-title>
        </v-list-item>
        <v-list-item to="/joinus">
          <v-list-item-title>Join Us</v-list-item-title>
        </v-list-item>
        <v-list-item to="/squadron">
          <v-list-item-title>Squadrons</v-list-item-title>
        </v-list-item>
        <div v-if="isLoggedIn">
          <v-list-item to="/documentation/list">
            <v-list-item-title>Documentation</v-list-item-title>
          </v-list-item>
          <v-list-item to="/qualification/list">
            <v-list-item-title>Training Qualifications</v-list-item-title>
          </v-list-item>
          <v-list-item to="/schedule">
            <v-list-item-title>JTF Schedule</v-list-item-title>
          </v-list-item>
          <v-list-item to="/server">
            <v-list-item-title>Servers</v-list-item-title>
          </v-list-item>
          <v-list-item to="/operation">
            <v-list-item-title>Operations</v-list-item-title>
          </v-list-item>
        </div>
      </v-list>
      <FooterComponent/>
    </v-navigation-drawer>
    <v-main>
      <v-container class="fill-height" fluid>
        <v-row justify="center" align="center">
          <router-view></router-view>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import LoginComponent from "@/components/LoginComponent";
import FooterComponent from "@/components/FooterComponent";
import { ref } from "vue";

export default {
  name: "TitleView",
  components: { FooterComponent, LoginComponent },
  props: {
    source: String,
  },
  data: () => ({
    drawer: true,
  }),
  computed: {
    ...mapGetters([
      "squadrons",
      "hqs",
      "isLoggedIn",
      "tokenExpiration",
      "isAdmin",
    ]),
    adminLink: function () {
      if (window.location.hostname === "localhost") {
        return "http://localhost:8000/admin/";
      } else {
        return `https://${window.location.hostname}/admin/`;
      }
    },
  },
  methods: {
    ...mapActions(["getRoster", "getHQs", "getSquadrons", "getOperations"]),
  },
  watch: {
    $route(to) {
      document.title = to.meta.title || "JTF-191";
    },
  },
  setup() {
    const theme = ref("light");

    return {
      theme,
      toggleTheme: () =>
        (theme.value = theme.value === "light" ? "dark" : "light"),
    };
  },
  mounted() {
    this.getRoster();
    this.getSquadrons();
    this.getHQs();
    this.getOperations();
  },
};
</script>

<style lang="scss">
@import "src/assets/css/app.scss";
</style>

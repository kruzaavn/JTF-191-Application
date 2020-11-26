<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="75vw">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
              v-if="$route.name === 'Register'"
          ></v-btn>
        <v-btn
            v-else-if="isLoggedIn"
            color="white"
            outlined
            tile
            depressed
            @click="logout"
        >
          <v-icon left>mdi-logout</v-icon>{{ user.username }}
        </v-btn>
        <v-btn
            v-else
            color="white"
            outlined
            tile
            depressed
            v-bind="attrs"
            v-on="on"
        >
          <v-icon left>mdi-login</v-icon>Login
        </v-btn>
      </template>
      <v-card>
        <v-card-title primary-title>
          <h2>Login</h2>
        </v-card-title>

        <v-card-text>
          <v-form @submit.prevent="submit">
            <v-text-field
                v-model="credentials.username"
                prepend-icon="mdi-account"
                label="username"
            />
            <v-text-field
                :prepend-icon="show_password ? 'mdi-eye' : 'mdi-eye-off'"
                v-model="credentials.password"
                label="password"
                :type="show_password ? 'text' : 'password'"
                @click:prepend="show_password = !show_password"
            />
          </v-form>
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <!--          <router-link to="/register" style="margin-left: 2em">-->
          <!--            don't have a login? sign up here-->
          <!--          </router-link>-->
          <v-spacer></v-spacer>
          <v-btn
              outlined
              color="info"
              type="submit"
              value="submit"
              v-on:click="submit"
          >
            Login
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'Login',
  data() {
    return {
      dialog: false,
      show_password: false,
      credentials: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    ...mapActions(['login', 'logout']),
    submit() {
      this.login(this.credentials)
      this.dialog = false
    },
  },
  computed: {
    ...mapGetters(['user', 'isLoggedIn']),
  },
}
</script>

<style scoped></style>

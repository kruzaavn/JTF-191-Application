<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="500">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          v-if="!user"
          color="white"
          outlined
          tile
          depressed
          v-bind="attrs"
          v-on="on"
        >
          <v-icon left>mdi-login</v-icon>Login
        </v-btn>
        <v-btn
          v-if="user"
          color="white"
          outlined
          tile
          depressed
          @click="logout"
        >
          <v-icon left>mdi-logout</v-icon>{{ user.username }}
        </v-btn>
      </template>
      <v-card>
        <v-card-title primary-title>
          <h2>Login</h2>
        </v-card-title>

        <v-card-text>
          <v-form @submit.prevent="submit">
            <v-text-field
              v-model="username"
              prepend-icon="mdi-account"
              label="username"
            />
            <v-text-field
              :prepend-icon="show_password ? 'mdi-eye' : 'mdi-eye-off'"
              v-model="password"
              label="password"
              :type="show_password ? 'text' : 'password'"
              @click:prepend="show_password = !show_password"
            />
          </v-form>
        </v-card-text>
        <v-divider />
        <v-card-actions>
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
      username: '',
      password: '',
    }
  },
  methods: {
    ...mapActions(['login', 'logout']),
    submit() {
      this.login({ username: this.username, password: this.password })
      this.dialog = false
    },
  },
  computed: {
    ...mapGetters(['user']),
  },
}
</script>

<style scoped></style>

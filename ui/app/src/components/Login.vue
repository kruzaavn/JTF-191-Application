<template>

 <div class="text-center">
    <v-dialog
      v-model="dialog"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="white"
          outlined
          v-bind="attrs"
          v-on="on"
        >
          <v-icon left>mdi-login</v-icon>Login
        </v-btn>
      </template>

      <v-card>
        <v-card-title
          primary-title
        >
          <h2>Login</h2>
        </v-card-title>
        <v-card-text>
        <v-form>
          <v-text-field v-model="username"
                        prepend-icon="mdi-account"
                        label="username"></v-text-field>
          <v-text-field :prepend-icon="show_password ? 'mdi-eye' : 'mdi-eye-off'"
                        v-model="password"
                        label="password"
                        :type="show_password ? 'text': 'password'"
                        @click:prepend="show_password = !show_password"
          ></v-text-field>
          {{jwt}} {{username}} {{password}}
        </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn outlined>Register</v-btn>
          <v-spacer></v-spacer>
          <v-btn outlined color="info">Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>


</template>

<script>
    import {mapActions, mapGetters} from 'vuex';
    export default {
        name: "Login",
        data() {
          return {
            dialog: false,
            show_password: false,
            username: 'aas',
            password: 'bba',
          }
        },
        method: {
          ...mapActions(['fetchJWT'])
        },
        computed: {
          ...mapGetters(['jwt', 'jwtData', 'jwtSubject', 'jwtIssuer'])
        }
    }
</script>

<style scoped>

</style>
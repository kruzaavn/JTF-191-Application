<template>
  <div class="text-center">
    <v-menu offset-y v-if="isLoggedIn">
      <template v-slot:activator="{ on }">
        <v-btn v-on="on">
          {{ user.username }}
          <v-icon right>fa-chevron-circle-down fa-xs</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item @click="redirect('/profile')">
          <v-list-item-title>My Profile</v-list-item-title>
        </v-list-item>
        <v-list-item
          @click="
            logout();
            redirect('/');
          "
        >
          <v-list-item-title>LogOut</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-btn v-if="!isLoggedIn">
      <v-icon left>mdi-login</v-icon>
      Login
      <v-dialog v-model="dialog" activator="parent">
        <v-card>
          <v-card-title primary-title>
            <h2>Login</h2>
          </v-card-title>

          <v-card-text>
            <v-form @submit.prevent="submit" ref="form">
              <v-text-field
                v-model="credentials.username"
                prepend-icon="mdi-account"
                label="username"
                :rules="[rules.blank]"
              />
              <v-text-field
                :prepend-icon="show_password ? 'mdi-eye' : 'mdi-eye-off'"
                v-model="credentials.password"
                label="password"
                :rules="[rules.blank]"
                :type="show_password ? 'text' : 'password'"
                @click:prepend="show_password = !show_password"
              />
            </v-form>
          </v-card-text>
          <v-divider />
          <v-card-actions>
            <v-alert v-if="errors" dense outlined type="warning">
              {{ errors.detail }}
            </v-alert>
            <v-spacer></v-spacer>
            <v-btn
              outlined
              color="info"
              type="submit"
              value="submit"
              @click="submit"
            >
              Login
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-btn>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "LoginComponent",
  data() {
    return {
      dialog: false,
      show_password: false,
      credentials: {
        username: "",
        password: "",
      },
      errors: null,
      rules: {
        blank: (v) => v.length > 0 || "must not be blank",
      },
    };
  },
  methods: {
    ...mapActions(["login", "logout", "getUser"]),
    submit() {
      if (this.$refs.form.validate()) {
        this.login(this.credentials)
          .then(() => {
            this.getUser();
            this.dialog = false;
          })
          .catch((error) => {
            this.errors = error.response.data;
          });
      }
    },
    redirect(path) {
      this.$router.push(path).catch(() => {});
    },
  },

  computed: {
    ...mapGetters(["user", "isLoggedIn", "isAdmin"]),
  },
};
</script>

<style scoped></style>

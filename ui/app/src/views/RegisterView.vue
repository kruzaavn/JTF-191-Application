<template>
  <v-container style="min-height: 100vh">
    <div id="registrationForm" v-if="!submitted">
      <h1>
        User Registration for
        {{ aviator.callsign }}
      </h1>
      <v-form ref="form">
        <v-row>
          <v-col>
            <v-text-field
              v-model="registerForm.username"
              label="Username"
              :rules="[rules.blank]"
            >
            </v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="registerForm.password"
              type="password"
              label="Password"
              :rules="[rules.blank, rules.minimumLength]"
            >
            </v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="validatePassword"
              type="password"
              label="Retype Password"
              :rules="[passwordMatchesRule, rules.blank]"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-alert
              v-for="(error, propertyName) in errors"
              :key="propertyName"
              dense
              outlined
              type="warning"
            >
              {{ error[0] }}
            </v-alert>
          </v-col>
          <v-col align="end">
            <v-btn outlined tile color="Submit" v-on:click="postApplication"
              >Submit</v-btn
            >
          </v-col>
        </v-row>
      </v-form>
    </div>
    <div id="" v-else>
      <h1>You have been successfully registered!</h1>
      <p>
        Returning to the homepage, if you aren't redirected click
        <router-link to="/">here</router-link>
      </p>
    </div>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import axios from "axios";
import router from "../router";

export default {
  name: "RegisterView",
  props: ["id"],
  mounted() {
    this.getAviator(this.id);
  },
  computed: {
    ...mapGetters(["aviator"]),
    passwordMatchesRule() {
      return () =>
        this.registerForm.password === this.validatePassword ||
        "Password must match";
    },
  },
  methods: {
    ...mapActions(["getAviator"]),
    postApplication: function () {
      if (this.$refs.form.validate()) {
        axios
          .post(`/api/roster/users/create/${this.id}/`, this.registerForm)
          .then(() => {
            this.submitted = true;
            router.push("/");
          })
          .catch((error) => {
            this.errors = error.response.data;
          });
      }
    },
  },
  data: () => ({
    registerForm: {
      // form data for api submission, changed variable style to
      // api format.
      username: "",
      password: "",
    },
    validatePassword: "",
    errors: null,
    submitted: false,
    rules: {
      blank: function (v) {
        return v.length > 0 || "must not be blank";
      },
      minimumLength: function (v) {
        return v.length >= 8 || "password must be at least 8 characters long";
      },
    },
  }),
};
</script>

<style></style>

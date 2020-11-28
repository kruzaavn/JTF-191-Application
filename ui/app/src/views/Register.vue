<template>
  <v-container>
    <div id="registrationform" v-if="!submitted">
      <h1>User Registration</h1>
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
      <p>Returning to the homepage, if you aren't redirected click <router-link to="/">here</router-link></p>
    </div>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import axios from 'axios'

export default {
  name: 'Register',
  computed: {
    ...mapGetters(['dcsModules']),
    passwordMatchesRule() {
      return () => (this.registerForm.password === this.validatePassword) || 'Password must match'
    }
  },
  methods: {
    ...mapActions(['getDcsModules']),
    postApplication: function () {
      if (this.$refs.form.validate()) {
        axios
          .post('/api/roster/users/create/', this.registerForm)
          .then(() => (this.submitted = true))
          .catch((response) => console.log(response.data))
      }
    },
  },
  data: () => ({
    registerForm: {
      // form data for api submission, changed variable style to
      // api format.
      username: '',
      password: '',
    },
    validatePassword: '',
    errors: [],
    submitted: false,
    rules: {
      blank: function (v) { return v.length > 0 || 'must not be blank' },
      minimumLength: function (v) { return  v.length >= 8 || 'password must be at least 8 characters long'}
    },
  }),
}
</script>

<style></style>

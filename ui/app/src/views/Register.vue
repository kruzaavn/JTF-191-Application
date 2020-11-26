<template>
  <v-container>
    <div id="registrationform" v-if="!submitted">
      <v-form ref="form">
        <v-row>
          <v-col>
            <v-text-field
              v-model="registerForm.username"
              label="Username"
              :rules="rules.blank"
            >
            </v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="registerForm.password"
              type="password"
              label="Password"
              :rules="rules.blank"
            >
            </v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="validatePassword"
              type="password"
              label="Retype Password"
              :rules="rules.matches"
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
      <h1>Thank you {{ joinUsForm.callsign }}</h1>
      <p>
        Your application has been submitted. Watch your email at
        <strong>{{ joinUsForm.email }}</strong> for an confirmation and thank
        you for your interest.
      </p>
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
  },
  methods: {
    ...mapActions(['getDcsModules']),
    postApplication: function () {
      if (this.$refs.form.validate()) {
        axios
          .post('/api/roster/prospective_aviators/detail/', this.joinUsForm)
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
      blank: [(v) => v.length > 0 || 'must not be blank'],
      matches: [(v) => (v === this.registerForm.password) || "passwords do not match"]
    },
  }),
}
</script>

<style></style>

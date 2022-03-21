<template>
  <v-container>
    <div id="joinusform" v-if="!submitted">
      <h1>Join Us</h1>
      <p>Requirements to join JTF-191</p>
      <v-list>
        <v-list-item>18 years or older</v-list-item>
        <v-list-item>Cockpit visualization, VR headset or Track IR</v-list-item>
        <v-list-item>Hands on throttle and stick (HOTAS)</v-list-item>
        <v-list-item>
          Be able to attend make required time commitments, approximately 2-3
          nights a week for 2 hours at 8pm Eastern time including a Mission
          Night on Saturday.
        </v-list-item>
        <v-list-item>
          Have a good attitude and a willingness to learn.
          <router-link to="/about">see our core values</router-link>
        </v-list-item>
      </v-list>
      <v-form ref="form">
        <v-row>
          <v-col>
            <v-row>
              <v-checkbox
                v-model="age"
                :rules="[(v) => !!v || 'You must be over the age of 18!']"
                label="Are you over 18?"
              ></v-checkbox>
            </v-row>
            <v-row>
              <v-checkbox
                v-model="valueStatement"
                :rules="[(v) => !!v || 'You must read out statement of values']"
                label="Have you read our Statement of Values?"
              ></v-checkbox>
            </v-row>
            <v-row>
              <!--                        Doing a timezone drop down menu is a huge headache-->
              <v-checkbox
                v-model="attendance"
                :rules="[
                  (v) => !!v || 'You must be able to make the time commitment',
                ]"
                label="Are you able make the required time commitment?"
              ></v-checkbox>
            </v-row>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              v-model="joinUsForm.first_name"
              label="First Name"
              :rules="rules.blank"
            >
            </v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="joinUsForm.last_name"
              label="Last Name"
              :rules="rules.blank"
            >
            </v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="joinUsForm.email"
              type="email"
              label="E-mail"
              :rules="[(v) => v.includes('@') || 'must be an email']"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              v-model="joinUsForm.callsign"
              label="Callsign"
              :rules="rules.blank"
            >
            </v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="joinUsForm.hotas"
              label="Type of HOTAS"
              :rules="rules.blank"
            >
            </v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="joinUsForm.head_tracking"
              label="Type of Head tracking or VR"
              :rules="rules.blank"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              v-model="joinUsForm.discord"
              label="Discord Name (e.g. Payno#1234)"
              :rules="rules.blank"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col cols="12" sm="6">
            <v-select
              v-model="joinUsForm.dcs_modules"
              :items="filterModulesByType('aircraft')"
              :menu-props="{ maxHeight: '400' }"
              label="Airframes"
              multiple
              hint="Pick your owned airframes"
              persistent-hint
              item-text="text"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6">
            <v-select
              v-model="joinUsForm.preferred_airframe"
              :items="filterModulesByType('aircraft')"
              :menu-props="{ maxHeight: '400' }"
              label="Preferred Airframe"
              hint="Select the airframe you intend to start training with"
              persistent-hint
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6">
            <v-select
              v-model="joinUsForm.dcs_modules"
              :items="filterModulesByType('map')"
              :menu-props="{ maxHeight: '400' }"
              label="Maps"
              multiple
              hint="Pick your owned maps"
              persistent-hint
            ></v-select>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-textarea
              v-model="joinUsForm.about"
              auto-grow
              clearable
              label="Tell Us about yourself"
              hint="Briefly describe what you are looking for and how we are a good fit for you?"
              rows="1"
            >
            </v-textarea>
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
import { mapGetters, mapActions } from "vuex";
import axios from "axios";
export default {
  name: "JoinUs",
  computed: {
    ...mapGetters(["dcsModules"]),
  },
  methods: {
    ...mapActions(["getDcsModules"]),
    postApplication: function () {
      if (this.$refs.form.validate()) {
        axios
          .post("/api/roster/prospective_aviators/detail/", this.joinUsForm)
          .then(() => (this.submitted = true))
          .catch((response) => console.log(response.data));
      }
    },
    filterModulesByType: function (type) {
      let modules = this.dcsModules.filter((x) => x.module_type === type);
      let selectable = [];

      for (const module of modules) {
        selectable.push({
          text: module.name || module.dcs_display_name,
          value: module.id,
          disabled: false,
        });
      }
      return selectable;
    },
  },
  mounted() {
    this.getDcsModules();
  },
  data: () => ({
    joinUsForm: {
      // form data for api submission, changed variable style to
      // api format.
      first_name: "",
      last_name: "",
      email: "",
      callsign: "",
      hotas: "",
      head_tracking: "",
      dcs_modules: [],
      about: "",
      discord: "",
      preferred_airframe: "",
    },
    attendance: false,
    age: false,
    valueStatement: false,
    submitted: false,
    rules: {
      blank: [(v) => v.length > 0 || "must not be blank"],
    },
  }),
};
</script>

<style></style>

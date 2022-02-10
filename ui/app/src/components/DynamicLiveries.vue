<template>
  <v-card class="mx-4 my-5 py-2" tile>
    <v-card-title>Livery actions</v-card-title>
    <v-card-text>
      <div>To download the most up to date liveries please use the button below. Make sure to unzip and move the content of the "liveries" folder into your DCS folder.</div>
      <div v-if="isAdmin">To create a new livery package, please click the button below. This will recreate all the aviators' liveries 
        and store them in our database. Anybody can then click the "Download livery package" button to get the updated ones.</div>
    </v-card-text>
    <v-card-actions class="justify-center">
      <v-btn
        outlined
        tile
        depressed
        :disabled="processing"
        @click="downloadLiveryPackage"
      >
        Download livery package
      </v-btn>
      <v-btn
        outlined
        tile
        depressed
        :disabled="processing"
        @click="createLiveryPackage"
        v-if="isAdmin"
      >
        Create livery package
      </v-btn>
    </v-card-actions>
    <v-container v-if="processing">
      <v-row class="text-center">
        <v-col cols="12">
          Plase wait until the action is complete...
        </v-col>
      </v-row>
      <v-row class="justify-center">
        <v-col cols="12">
          <v-progress-linear
            color="deep-purple accent-4"
            indeterminate
            rounded
            height="6"
            width="80%"
          ></v-progress-linear>
        </v-col>
      </v-row>
    </v-container>
    <v-snackbar
      v-model="show_snackbar"
      :timeout="snackbar_timeout"
    >
      {{ snackbar_text }}

      <template v-slot:action="{ attrs }">
        <v-btn
          color="blue"
          text
          v-bind="attrs"
          @click="snackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-card>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import axios from 'axios'

export default {
  name: 'DynamicLiveries',
  data() {
    return {
      processing: false,
      show_snackbar: false,
      snackbar_text: "",
      snackbar_timeout: 2000,
      timer: null,
    }
  },
  computed: {
    ...mapGetters(['aviator', 'user', 'isAdmin', 'rqToken']),
  },
  mounted() {
    this.getUser().then(() => {
      this.getAviatorFromUser(this.user.id)
    })
    .catch((error) => {
      console.log(error)
    })
  },
  methods: {
    ...mapActions(['getAviatorFromUser', 'getUser']),
    downloadLiveryPackage() {
      this.processing = true
      axios({
        url: `/api/roster/liveries/update/`,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        if (response.data.size > 0) {
            var fileURL = window.URL.createObjectURL(new Blob([response.data]))
            var fileLink = document.createElement('a')
            
            fileLink.href = fileURL
            fileLink.setAttribute('download', 'liveries.zip')
            document.body.appendChild(fileLink)
            
            fileLink.click();

            this.snackbar_text = "Downloading file..."
            this.show_snackbar = true
        } else {
          this.snackbar_text = "No file returned..."
          this.show_snackbar = true
        }
        this.processing = false
      })
      .catch((error) => {
        console.log(error)
        this.processing = false
        this.snackbar_text = "Error while downloading the livery package."
        this.show_snackbar = true
      })
    },
    createLiveryPackage() {
      this.processing = true
      axios({
        url: `/api/roster/liveries/update/`,
        method: 'POST'
      }).then(() => {
        this.snackbar_text = "Process started..."
        this.show_snackbar = true
        this.processing = false
      })
      .catch((error) => {
        console.log(error)
        this.processing = false
        this.snackbar_text = "Error while creating the livery package."
        this.show_snackbar = true
      })
    }
  }
}
</script>

<style>
</style>
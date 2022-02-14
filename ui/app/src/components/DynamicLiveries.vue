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
      <v-btn
        outlined
        tile
        depressed
        v-if="isAdmin"
        @click="show_stats = !show_stats"
      >
        Show/Hide previous run stats
      </v-btn>
    </v-card-actions>
    <v-container v-if="show_stats">
      <v-row class="text-left">
        <v-col cols="12">
          <v-simple-table>
            <template v-slot:default>
              <tbody>
                <tr>
                  <td>Completed jobs</td>
                  <td>{{ finished_jobs }}</td>
                </tr>
                <tr>
                  <td>Scheduled jobs</td>
                  <td>{{ scheduled_jobs }}</td>
                </tr>
                <tr>
                  <td>Failed jobs</td>
                  <td>{{ falied_jobs }}</td>
                </tr>
                <tr>
                  <td>In progress jobs</td>
                  <td>{{ started_jobs }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-col>
      </v-row>
    </v-container>
    <v-container v-if="processing">
      <v-row class="text-center">
        <v-col cols="12">
          Plase wait until the action is complete...
        </v-col>
      </v-row>
      <v-row class="justify-center">
        <v-col cols="12">
          <v-progress-linear
            rounded
            height="6"
            width="80%"
            :value="progress"
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
          @click="show_snackbar = false"
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
      snackbar_timeout: 1000,
      timer: null,
      livery_job_ids: [],
      started_jobs: 0,
      finished_jobs: 0,
      falied_jobs: 0,
      scheduled_jobs: 0,
      show_stats: false,
      progress: 0
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
      }).then((response) => {
        // Get job ids
        this.livery_job_ids = response.data

        // Reset stats
        this.show_stats = true
        this.scheduled_jobs = this.livery_job_ids.length
        this.started_jobs = 0
        this.finished_jobs = 0
        this.falied_jobs = 0

        this.snackbar_text = `Success: ${this.scheduled_jobs} jobs scheduled...`
        this.show_snackbar = true
        this.timer = setInterval(function () {
          this.checkQueue()
        }.bind(this), 2000);
      })
      .catch((error) => {
        console.log(error)
        this.processing = false
        this.snackbar_text = error
        this.show_snackbar = true
      })
    },
    checkQueue() {
      axios({
        url: `/api/roster/rq/queue/status/`,
        method: 'POST',
        data: {
          'queue_name': 'liveries',
          'job_ids': this.livery_job_ids
        }
      }).then((response) => {
        this.started_jobs = response.data.started_jobs
        this.finished_jobs = response.data.finished_jobs
        this.falied_jobs = response.data.falied_jobs
        this.scheduled_jobs = response.data.scheduled_jobs

        this.progress = ((this.finished_jobs + this.falied_jobs) / this.livery_job_ids.length) * 100

        if (this.scheduled_jobs == 0 && this.started_jobs == 0) {
          this.snackbar_text = "Livery process complete"
          this.processing = false
          this.show_snackbar = true
          clearInterval(this.timer)
        }
      })
      .catch((error) => {
        this.processing = false
        this.snackbar_text = error
        this.show_snackbar = true
        clearInterval(this.timer)
      })
    }
  },
  beforeDestroy() {
    clearInterval(this.timer)
  }
}
</script>

<style>
</style>
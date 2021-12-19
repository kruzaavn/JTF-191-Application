<template>
  <v-card class="mx-4 my-5 py-2" tile>
    <v-container>
      <v-row>
        <v-col>
          <v-row>
            <v-col>
              <v-btn
                v-if="isAdmin"
                outlined
                tile
                depressed
                :disabled="processingLiveries"
                @click="reloadLiveries"
              >
                Download liveries
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
    <v-container v-if="processingLiveries">
      <v-row class="text-center">
        <v-col cols="12">
          Getting your liveries, please do not close the browser.
          A download will start once the livery package is ready.
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
  </v-card>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import axios from 'axios'

export default {
  name: 'DynamicLiveries',
  data() {
    return {
      processingLiveries: false,
    }
  },
  computed: {
    ...mapGetters(['aviator', 'user', 'isAdmin']),
  },
  mounted() {
    this.getUser().then(() => {
      this.getAviator(this.user.id)
    })
    .catch((error) => {
      console.log(error)
    })
  },
  methods: {
    ...mapActions(['getAviator', 'getUser']),
    reloadLiveries() {
      this.processingLiveries = true
      axios({
        url: `/api/roster/liveries/update/`,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        if (response.data.size > 0) {
            var fileURL = window.URL.createObjectURL(new Blob([response.data]));
            var fileLink = document.createElement('a');
            
            fileLink.href = fileURL;
            fileLink.setAttribute('download', 'aviator_liveries.zip');
            document.body.appendChild(fileLink);
            
            fileLink.click();
        } else {
          console.log('No file returned')
        }
        this.processingLiveries = false
      })
      .catch((error) => {
        console.log(error)
        this.processingLiveries = false
      })
    }
  }
}
</script>

<style>
</style>
<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>Flight Schedule</h1>
        <v-sheet height="1000">
          <v-calendar
            :events="schedule"
            color="primary"
            :event-color="eventColor"
          ></v-calendar>
        </v-sheet>
      </v-col>
    </v-row>
    <v-row> </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Schedule',
  computed: {
    ...mapGetters(['schedule']),
  },
  methods: {
    ...mapActions(['getSchedule']),
    eventColor(event) {
      if (event.type === 'training') {
        return 'green'
      } else {
        return 'yellow'
      }
    },
  },
  mounted() {
    this.getSchedule()
  },
}
</script>

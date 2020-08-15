<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>JTF Schedule</h1>
        <v-sheet tile height="54" color="grey lighten-3" class="d-flex">
          <!--          <v-btn icon class="ma-2" @click="prev()">-->
          <!--            <v-icon>mdi-chevron-left</v-icon>-->
          <!--          </v-btn>-->
          <v-spacer></v-spacer>
          <!--          <v-btn icon class="ma-2" @click="next()">-->
          <!--            <v-icon>mdi-chevron-right</v-icon>-->
          <!--          </v-btn>-->
        </v-sheet>
        <v-sheet height="1000">
          <v-calendar
            ref="calendar"
            :events="schedule"
            color="primary"
            event-more
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
      } else if (event.type === 'admin') {
        return 'purple'
      } else {
        return 'blue'
      }
    },
    prev() {
      this.$refs.calendar.prev()
    },
    next() {
      this.$refs.calendar.next()
    },
  },
  mounted() {
    this.getSchedule()
  },
}
</script>

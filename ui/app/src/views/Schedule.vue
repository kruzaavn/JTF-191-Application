<template>
  <v-container>
    <v-row v-if="schedule">
      <v-col>
        <h1>JTF Schedule</h1>
        <v-sheet tile height="64">
          <v-toolbar flat>
            <v-btn icon class="ma-2" @click="prev()">
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
            <v-toolbar-title v-if="$refs.calendar">
              {{ $refs.calendar.title }}
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon class="ma-2" @click="next()">
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-toolbar>
        </v-sheet>
        <v-sheet height="1000">
          <v-calendar
            ref="calendar"
            :events="schedule"
            color="primary"
            event-more
            :event-color="eventColor"
            @click:event="showEvent"
            v-model="value"
          ></v-calendar>
          <v-menu
            v-model="selectedOpen"
            :close-on-content-click="false"
            :activator="selectedElement"
            min-width="400px"
            offset-x
            tile
          >
            <v-card color="grey lighten-4" min-width="400px" tile>
              <v-toolbar :color="eventColor(selectedEvent)" dark>
                <v-toolbar-title
                  >{{ selectedEvent.type | capitalize }}:
                  {{ selectedEvent.name }}</v-toolbar-title
                >
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>
                <p>{{ selectedEvent.description }}</p>
              </v-card-text>
              <v-list color="grey lighten-4" dense>
                <v-subheader>Required Squadrons</v-subheader>
                <v-list-item
                  v-for="squadron in selectedEvent.required_squadrons"
                  :key="squadron.id"
                  ><v-list-item-subtitle
                    v-text="squadron.designation"
                    class="text-caption my-1"
                  >
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
              <v-card-actions>
                <v-btn text color="secondary" @click="selectedOpen = false">
                  Close
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-menu>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Schedule',
  data: () => ({
    value: '',
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
  }),

  computed: {
    ...mapGetters(['schedule']),
  },
  filters: {
    capitalize: function (value) {
      if (!value) return ''
      value = value.toString()
      return value.charAt(0).toUpperCase() + value.slice(1)
    },
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
    showEvent({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = event
        this.selectedElement = nativeEvent.target
        setTimeout(() => (this.selectedOpen = true), 10)
      }

      if (this.selectedOpen) {
        this.selectedOpen = false
        setTimeout(open, 10)
      } else {
        open()
      }

      nativeEvent.stopPropagation()
    },
  },
  mounted() {
    this.getSchedule()
  },
}
</script>

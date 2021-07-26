<template>
  <v-container height="100%">
    <v-row>
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
            <Event />
            <v-btn icon class="ma-2" @click="next()">
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-toolbar>
        </v-sheet>
        <v-sheet height="90vh">
          <v-calendar
            ref="calendar"
            :events="formattedSchedule"
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
            max-width="500px"
            offset-x
            tile
          >
            <v-card
              color="grey lighten-4"
              min-width="400px"
              max-width="500px"
              tile
            >
              <v-toolbar :color="eventColor(selectedEvent)" dark>
                <v-toolbar-title
                  >{{ selectedEvent.type | capitalize }}:
                  {{ selectedEvent.name | capitalize }}</v-toolbar-title
                >
                <v-spacer></v-spacer>
              </v-toolbar>

              <v-card-subtitle>Event Description</v-card-subtitle>
              <v-card-text>
                <markdown-it-vue
                  :content="selectedEvent.description"
                ></markdown-it-vue>
              </v-card-text>

              <v-card-subtitle>Required Squadrons</v-card-subtitle>
              <v-chip
                v-for="squadron in selectedEvent.required_squadrons"
                :key="squadron.id"
                class="mx-1"
                outlined
                >{{ squadron.designation }}</v-chip
              >
              <v-card-actions>
                <UpdateEvent
                  v-on:clear="hideEvent"
                  :selected-event="selectedEvent"
                  :key="selectedEvent.id || -1"
                />
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
import Event from '@/components/Event'
import UpdateEvent from '@/components/UpdateEvent'

export default {
  name: 'Schedule',
  components: { Event, UpdateEvent },
  data: () => ({
    value: '',
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
  }),

  computed: {
    ...mapGetters(['schedule']),
    formattedSchedule: function () {
      let events = []

      for (const event of this.schedule) {
        let new_event = { ...event }

        new_event.start = this.formatDate(event.start)
        new_event.end = this.formatDate(event.end)

        events.push(new_event)
      }

      return events
    },
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
    formatDate: function (dateString) {
      let date = new Date(dateString)

      let elements = [
        date.getFullYear(),
        date.getMonth() + 1,
        date.getDate(),
        date.getHours(),
        date.getMinutes(),
      ]
      let strings = []

      for (const element of elements) {
        if (element < 10) {
          strings.push(`0${element}`)
        } else {
          strings.push(`${element}`)
        }
      }

      return `${strings[0]}-${strings[1]}-${strings[2]} ${strings[3]}:${strings[4]}`
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
    hideEvent() {
      this.selectedOpen = false
    },
  },
  mounted() {
    setTimeout(() => {
      this.getSchedule()
    }, 250)
  },
}
</script>

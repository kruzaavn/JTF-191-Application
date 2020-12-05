<template>
  <div>
    <v-dialog v-model="dialog" max-width="900px" min-width="50vw">
      <template v-slot:activator="{ on, attrs }">
        <v-btn outlined tile depressed v-bind="attrs" v-on="on">
          Manage Event
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="headline">
          Manage {{ selectedEvent.name }}
        </v-card-title>
        <v-form ref="selectedEventForm">
          <v-container>
            <v-row>
              <v-col cols="5">
                <v-row>
                  <v-col>
                    <v-date-picker v-model="newEvent.date"></v-date-picker>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-text-field
                      name="startTime"
                      label="Start Time"
                      v-model="newEvent.start"
                      hint="24hr Format"
                      :rules="[rules.blank, rules.format24hrTime]"
                    ></v-text-field>
                  </v-col>
                  <v-col>
                    <v-text-field
                      label="Duration"
                      v-model="newEvent.duration"
                      hint="(H)H:MM"
                      :rules="[rules.blank, rules.formatTime]"
                    ></v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-select
                      label="Type"
                      v-model="newEvent.eventType"
                      :items="eventTypes"
                    >
                    </v-select>
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="7">
                <v-text-field
                  v-model="newEvent.name"
                  label="Event Name"
                  :rules="[rules.blank]"
                ></v-text-field>
                <v-select
                  label="Required squadrons"
                  v-model="newEvent.squadrons"
                  :items="squadrons"
                  item-text="designation"
                  item-value="id"
                  chips
                  deletable-chips
                  multiple
                ></v-select>
                <v-textarea
                  v-model="newEvent.description"
                  label="Event Description"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
        <v-card-actions>
          <v-btn
            color="red"
            outlined
            tile
            depressed
            @click="
              deleteEvent()
              $emit('clear')
            "
          >
            Delete Event
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            outlined
            tile
            depressed
            @click="
              updateEvent()
              $emit('clear')
            "
          >
            Update Event
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

function DefaultNewEvent() {
  this.date = new Date().toLocaleDateString('en-CA')
  this.start = '12:00'
  this.duration = '0:30'
  this.squadrons = []
  this.eventType = 'admin'
  this.name = ''
}

export default {
  name: 'UpdateEvent',
  props: ['selectedEvent'],
  computed: {
    ...mapGetters(['squadrons']),
  },
  methods: {
    ...mapActions(['addToSchedule', 'removeFromSchedule', 'updateSchedule']),
    deleteEvent: function () {
      if (this.$refs.selectedEventForm.validate()) {
        this.removeFromSchedule(this.formatEvent()).then(
          () => (this.dialog = false)
        )
      }
    },
    updateEvent: function () {
      if (this.$refs.selectedEventForm.validate()) {
        if (this.$refs.selectedEventForm.validate()) {
          this.updateSchedule(this.formatEvent()).then(
            () => (this.dialog = false)
          )
        }
      }
    },
    formatEvent: function () {
      let yymmdd = this.newEvent.date.split('-').map((x) => parseInt(x))
      yymmdd[1]--
      let hhmm = this.newEvent.start.split(':').map((x) => parseInt(x))

      let start = new Date(...yymmdd, ...hhmm)
      let ohhmm = this.newEvent.duration
        .split(':')
        .map((x) => parseInt(x) * 1000)
      let offset = ohhmm[0] * 3600 + ohhmm[1] * 60
      let end = new Date(start.getTime() + offset)

      return {
        id: this.newEvent.id,
        start: start.toJSON(),
        end: end.toJSON(),
        description: this.newEvent.description,
        required_squadrons: this.newEvent.squadrons,
        type: this.newEvent.eventType,
        name: this.newEvent.name,
      }
    },
    formatSelectedEvent: function () {
      if (this.selectedEvent) {
        const event = { ...this.selectedEvent }
        const start = new Date(event.start)
        const end = new Date(event.end)
        const diff = (end - start) / 1000
        const dHH = Math.floor(diff / 3600)
        const dMM = Math.floor((diff - dHH * 3600) / 60)

        return {
          date: start.toLocaleDateString('en-CA'),
          start: `${start.getHours()}:${start.getMinutes() || '00'}`,
          duration: `${dHH}:${dMM || '00'}`,
          description: event.description,
          name: event.name,
          eventType: event.type,
          squadrons: event.required_squadrons.map((x) => x.id),
          id: event.id,
        }
      } else {
        return new DefaultNewEvent()
      }
    },
  },
  data() {
    return {
      dialog: false,
      newEvent: (this.newEvent = this.formatSelectedEvent()),
      eventTypes: ['admin', 'training', 'operation'],
      rules: {
        blank: function (v) {
          return v.length > 0 || 'Must not be blank'
        },
        format24hrTime: function (v) {
          return (
            /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/.test(v) || 'Must be in 24hr time'
          )
        },
        formatTime: function (v) {
          return /\d+:[0-5][0-9]/.test(v) || 'Must be in (H)H:MM'
        },
      },
    }
  },
}
</script>

<style scoped></style>

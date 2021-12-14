<template>
  <v-dialog v-model="dialog" max-width="900px" min-width="50vw">
    <template v-slot:activator="{ on, attrs }">
      <v-btn outlined tile depressed v-bind="attrs" v-on="on">
        Add event
      </v-btn>
    </template>

    <v-card>
      <v-card-title class="headline">
        Schedule New Event
      </v-card-title>
      <v-form ref="newEventForm">
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
                  <v-select
                    label="Periodicity"
                    :items="periodicityTypes"
                    v-model="period.periodicity"
                  ></v-select>
                </v-col>
                <v-col>
                  <v-text-field
                    label="Duration"
                    v-model="newEvent.duration"
                    hint="(H)H:MM"
                    :rules="[rules.blank, rules.formatTime]"
                  ></v-text-field>
                  <v-text-field
                    label="Additional Repetitions"
                    v-model="period.number"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-col>
            <v-col cols="7">
              <v-text-field
                v-if="newEvent.eventType!='leave of absence'"
                v-model="newEvent.name"
                label="Event Name"
                :rules="[rules.blank]"
              ></v-text-field>
              <v-select
                label="Type"
                v-model="newEvent.eventType"
                :items="eventTypes"
              >
              </v-select>
              <v-select
                v-if="newEvent.eventType!='leave of absence'"
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
        <v-btn outlined tile depressed @click="clearNewEvent">
          Clear Event
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn outlined tile depressed @click="submitNewEvent">
          Create Event
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import dayjs from 'dayjs'

function DefaultNewEvent() {
  this.date = new Date().toLocaleDateString('en-CA')
  this.start = '12:00'
  this.duration = '0:30'
  this.squadrons = []
  this.eventType = 'admin'
  this.name = ''
}

function Period() {
  this.periodicity = null
  this.number = 0
}

export default {
  name: 'UpdateEvent',
  computed: {
    ...mapGetters(['squadrons', 'aviator', 'user']),
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
    ...mapActions(['addToSchedule', 'getAviator', 'getUser']),
    clearNewEvent: function () {
      this.newEvent = new DefaultNewEvent()
      this.period = new Period()
    },
    submitNewEvent: function () {
      if (this.$refs.newEventForm.validate()) {
        let formattedEvent = this.formatEvent()

        if (this.period.periodicity && this.period.number) {
          for (let i = 1; i < parseInt(this.period.number) + 1; i++) {
            let periodUpdatedEvent = { ...formattedEvent }

            if (this.period.periodicity === 'bw') {
              periodUpdatedEvent['start'] = dayjs(periodUpdatedEvent['start'])
                .add(i * 2, 'w')
                .toJSON()
              periodUpdatedEvent['end'] = dayjs(periodUpdatedEvent['end'])
                .add(i * 2, this.period.periodicity)
                .toJSON()
            } else {
              periodUpdatedEvent['start'] = dayjs(periodUpdatedEvent['start'])
                .add(i, this.period.periodicity)
                .toJSON()
              periodUpdatedEvent['end'] = dayjs(periodUpdatedEvent['end'])
                .add(i, this.period.periodicity)
                .toJSON()
            }

            this.addToSchedule(periodUpdatedEvent)
          }
        }

        // If the user is creating a new LOA we append
        // the aviator ID and the squadron automatically
        // We also default the name of the event to a standard
        // LOA - <CALLSIGN>
        if (this.newEvent.eventType == 'leave of absence') {
          formattedEvent['name'] = `LOA - ${this.aviator.callsign}`
          formattedEvent['aviator'] = this.aviator.id
          formattedEvent['required_squadrons'] = [this.aviator.squadron.id]
        }

        this.addToSchedule(formattedEvent).then(() => {
          this.clearNewEvent()
          this.dialog = false
        })
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
        start: start.toJSON(),
        end: end.toJSON(),
        description: this.newEvent.description,
        required_squadrons: this.newEvent.squadrons,
        type: this.newEvent.eventType,
        name: this.newEvent.name,
      }
    },
  },
  data() {
    return {
      dialog: false,
      newEvent: new DefaultNewEvent(),
      period: new Period(),
      eventTypes: ['admin', 'training', 'operation', 'leave of absence'],
      periodicityTypes: [
        { text: '---', value: null },
        { text: 'Weekly', value: 'w' },
        { text: 'Bi-Weekly', value: 'bw' },
        { text: 'Monthly', value: 'M' },
      ],
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

<template>
  <div>
    <v-dialog
        v-model="dialog"
        max-width="900px"
        min-width="50vw"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            outlined
            tile
            depressed
            v-bind="attrs"
            v-on="on"
        >
          Add Event
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
                    <v-text-field name="startTime"
                                  label="Start Time"
                                  v-model="newEvent.start"
                                  hint="12hr"
                                  :rules="[rules.blank, rules.format12hrTime]"
                    ></v-text-field>
                  </v-col>
                  <v-col>
                    <v-select
                        label="AM/PM"
                        v-model="newEvent.AMPM"
                        :items="selectAMPM"
                    >
                    </v-select>
                  </v-col>
                  <v-col>
                    <v-text-field
                        label="Duration"
                        v-model="newEvent.duration"
                        hint="HH:MM"
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
                <v-textarea
                    v-model="newEvent.description"
                    label="Event Description"
                ></v-textarea>
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
                {{newEvent}}
              </v-col>
            </v-row>
          </v-container>
        </v-form>
        <v-card-actions>
          <v-btn
              outlined
              tile
              depressed
              @click="clearNewEvent"
          >
            Clear Event
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
              outlined
              tile
              depressed
              @click="submitNewEvent"
          >
            Create Event
          </v-btn>
        </v-card-actions>
      </v-card>

    </v-dialog>
  </div>
</template>

<script>
import {mapGetters, mapActions} from "vuex";

function DefaultNewEvent() {
  this.date = null
  this.start = null
  this.AMPM = 'PM'
  this.duration = null
  this.squadrons =  []
  this.eventType = 'admin'
}

export default {
  name: "Event",
  computed: {
    ...mapGetters(['squadrons'])
  },
  methods: {
    ...mapActions(['addToSchedule']),
    clearNewEvent: function () {
      this.newEvent = new DefaultNewEvent()
    },
    submitNewEvent: function () {
      this.clearNewEvent()
      this.dialog = false
    }
  },
  data() {
    return {
      dialog: false,
      newEvent: new DefaultNewEvent(),
      selectAMPM: ['AM', 'PM'],
      eventTypes: ['admin', 'training', 'operation'],
      rules: {
        blank: function (v) { return v.length > 0 || 'Must not be blank'},
        format12hrTime: function (v) {return /^(0?[1-9]|1[0-2]):[0-5][0-9]$/.test(v) || 'Must be in 12hr time'},
        formatTime: function (v) {return /\d+:[0-5][0-9]/.test(v) || 'Must be in (H):MM' }
      }
    }
  }
}
</script>

<style scoped>

</style>
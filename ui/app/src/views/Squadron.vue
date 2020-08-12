<template>
  <v-container fluid>
    <v-row align-content="start">
      <v-col>
        <v-card class="py-4" tile>
          <v-img :src="squadron.img" contain height="500">
            <v-card-title>{{ squadronDesignation }}</v-card-title>
          </v-img>
          <v-card
            class="mx-4 my-5 py-2"
            v-for="member in members"
            :key="member.id"
            tile
          >
            <v-row>
              <v-col cols="2">
                <v-img
                  max-height="150"
                  contain
                  :src="
                    'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/' +
                    ranks[member.rank_code] +
                    '.svg'
                  "
                >
                </v-img>
              </v-col>
              <v-col>
                <v-card-title>
                  {{ member.rank }} {{ member.callsign }} {{ member.position }}
                </v-card-title>
                <v-card-subtitle>
                  Aircraft: {{ member.tail_number }} <br />
                  On board since {{ member.date_joined }} <br />
                  Status: {{ member.status }}
                </v-card-subtitle>
              </v-col>
            </v-row>
            <v-card-text>
              <v-row>
                <v-col>
                  <h4>
                    Total Flight Hours
                    {{ sumTable(member.stats.hours).toPrecision(2) }}
                  </h4>
                  <v-data-table
                    dense
                    :headers="hoursHeaders"
                    :items="toHoursTable(member.stats.hours)"
                  >
                  </v-data-table>
                </v-col>
                <v-col>
                  <h4>
                    Total kills
                    {{ sumTable(member.stats.kills).toPrecision(2) }}
                  </h4>
                  <v-data-table
                    dense
                    :headers="killsHeaders"
                    :items="toKillsTable(member.stats.kills)"
                  >
                  </v-data-table>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'Squadron',
  props: ['squadronDesignation'],
  data: () => ({
    ranks: {
      1: 'second_lieutenant',
      2: 'first_lieutenant',
      3: 'captain',
      4: 'major',
      5: 'lieutenant_colonel',
      6: 'colonel',
    },
    hoursHeaders: [
      {
        text: 'Airframe',
        align: 'start',
        sortable: true,
        value: 'airframe',
      },
      { text: 'Hours', value: 'hours' },
    ],
    killsHeaders: [
      {
        text: 'Victim',
        align: 'start',
        sortable: true,
        value: 'victim',
      },
      { text: 'Number', sortable: true, value: 'number' },
    ],
  }),
  computed: {
    ...mapGetters(['roster', 'squadrons']),
    members: function () {
      return this.roster.filter(
        (pilot) => pilot.squadron.designation === this.squadronDesignation
      )
    },
    squadron: function () {
      return this.squadrons.filter(
        (sqd) => sqd.designation === this.squadronDesignation
      )[0]
    },
  },
  filters: {
    upper: function (value) {
      return value.toUpperCase()
    },
  },
  methods: {
    toHoursTable(hours) {
      let data = []

      for (const airframe in hours) {
        data.push({ airframe: airframe, hours: hours[airframe].toPrecision(2) })
      }
      return data
    },
    toKillsTable(kills) {
      let data = []

      for (const victim in kills) {
        data.push({ victim: victim, number: kills[victim] })
      }
      return data
    },
    sumTable(obj) {
      let data = []

      for (const key in obj) {
        data.push(obj[key])
      }
      return data.reduce((a, b) => a + b, 0)
    },
  },
}
</script>

<style></style>

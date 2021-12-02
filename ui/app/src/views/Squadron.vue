<template>
  <v-container fluid>
    <v-row align-content="start">
      <v-col>
        <v-card class="py-4" tile>
          <v-img :src="squadron.img" contain height="500">
            <v-card-title>
              Name: {{ squadron.name }} <br />
              Tricode: {{ squadron.tri_code }} <br />
              Designation: {{ squadron.designation }} <br />
              Aircraft: {{ squadron.air_frame.name }} <br />
              Callsign: {{ squadron.callsign.toUpperCase() }} <br />
              Aviators: {{ members.length }}
            </v-card-title>
          </v-img>
          <v-card class="mx-4 my-5 py-2">
            <markdown-it-vue
              class="px-2"
              :content="squadron.description"
            ></markdown-it-vue>
          </v-card>

          <div v-for="member in members" :key="member.id">
            <v-card
              class="mx-4 my-5 py-2"
              v-if="member.status !== 'reserve'"
              tile
            >
              <v-row>
                <v-col cols="2">
                  <v-img
                    max-height="150"
                    contain
                    :src="ranks[member.rank_code.toString()]"
                  >
                  </v-img>
                </v-col>
                <v-col cols="4">
                  <v-card-title>
                    {{ member.rank }} {{ member.callsign }}
                    {{ member.position }}
                  </v-card-title>
                  <v-card-subtitle>
                    {{ member.squadron.tri_code }}{{ member.division }}-{{
                      member.division_position
                    }}|{{ member.callsign }}|{{ member.tail_number }} <br />
                    Aircraft: {{ member.tail_number }} <br />
                    On board since {{ member.date_joined }} <br />
                    Status: {{ member.status }}
                  </v-card-subtitle>
                </v-col>
                <v-col cols="4">
                  <v-row align="center" justify="center">
                    <v-col cols="4" v-for="award in sortAwards(member.awards)" :key="award.id" class="pa-0">
                      <v-img :src="award.ribbon_image_url" :alt="award.name"/>
                    </v-col>
                  </v-row>                  
                </v-col>
              </v-row>
              <v-card-text>
                <v-row>
                  <v-col>
                    <h4>
                      Total Flight Hours
                      {{ sumTable(member.stats.hours).toFixed(2) }}
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
                      {{ sumTable(member.stats.kills).toFixed(0) }}
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
          </div>
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
      '-4':
        'https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw1.svg',
      '-3':
        'https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw2.svg',
      '-2':
        'https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw3.svg',
      '-1':
        'https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw4.svg',
      '0':
        'https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw5.svg',
      '1':
        'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/second_lieutenant.svg',
      '2':
        'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/first_lieutenant.svg',
      '3':
        'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/captain.svg',
      '4':
        'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/major.svg',
      '5':
        'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/lieutenant_colonel.svg',
      '6':
        'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/colonel.svg',
    },
    hoursHeaders: [
      {
        text: 'Airframe',
        align: 'start',
        sortable: true,
        value: 'airframe',
      },
      { text: 'Hours', sortable: true, align: 'start', value: 'hours' },
    ],
    killsHeaders: [
      {
        text: 'Victim',
        align: 'start',
        sortable: true,
        value: 'victim',
      },
      { text: 'Number', sortable: true, align: 'start', value: 'number' },
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
        data.push({ airframe: airframe, hours: hours[airframe].toFixed(2) })
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
    sortAwards(awards) {
      return awards.slice().sort((a, b) => { return a.priority - b.priority})
    },
  },
}
</script>

<style></style>

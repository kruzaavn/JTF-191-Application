<template>
  <v-card class="mx-4 my-5 py-2" v-if="aviator.status !== 'reserve'" tile>
    <v-row>
      <v-col cols="2">
        <v-img
          max-height="150"
          contain
          :src="ranks[aviator.rank_code.toString()]"
        >
        </v-img>
      </v-col>
      <v-col cols="4">
        <v-card-title>
          {{ aviator.rank }} {{ aviator.callsign }}
          {{ aviator.position }}
        </v-card-title>
        <v-card-subtitle>
          {{ aviator.squadron.tri_code }}{{ aviator.division }}-{{
            aviator.division_position
          }}|{{ aviator.callsign }}|{{ aviator.tail_number }} <br />
          Aircraft: {{ aviator.tail_number }} <br />
          On board since {{ aviator.date_joined }} <br />
          Status: {{ aviator.status }}
        </v-card-subtitle>
      </v-col>
      <v-col cols="4">
        <v-row id="ribbon-rack" align="center" justify="center">
          <v-col
            cols="4"
            align="center"
            v-for="award in sortCitations(aviator.citations)"
            :key="award.id"
            class="pa-0"
          >
            <v-img :src="award.ribbon_image" :alt="award.name" />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-card-text>
      <v-row>
        <v-col>
          <h4>
            Total Flight Hours
            {{ sumTable(aviator.stats.hours).toFixed(2) }}
          </h4>
          <v-data-table
            dense
            :headers="hoursHeaders"
            :items="toHoursTable(aviator.stats.hours)"
          >
          </v-data-table>
        </v-col>
        <v-col>
          <h4>
            Total kills
            {{ sumTable(aviator.stats.kills).toFixed(0) }}
          </h4>
          <v-data-table
            dense
            :headers="killsHeaders"
            :items="toKillsTable(aviator.stats.kills)"
          >
          </v-data-table>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'AviatorSummary',

  props: {
      aviator: {
          type: Object,
          required: true
      }
  },
  data: () => ({
    ranks: {
      '-4': 'https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw1.svg',
      '-3': 'https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw2.svg',
      '-2': 'https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw3.svg',
      '-1': 'https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw4.svg',
      0: 'https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw5.svg',
      1: 'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/second_lieutenant.svg',
      2: 'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/first_lieutenant.svg',
      3: 'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/captain.svg',
      4: 'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/major.svg',
      5: 'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/lieutenant_colonel.svg',
      6: 'https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/colonel.svg',
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
    sortCitations(citations) {
      var groupByAward = (cits) =>
        cits.reduce(function (acc, x) {
          acc[x.award.id] = x.award
          return acc
        }, {})

      citations = citations.slice().sort((a, b) => {
        return b.award.priority - a.award.priority
      })

      return groupByAward(citations)
    },
  },
}
</script>

<style></style>

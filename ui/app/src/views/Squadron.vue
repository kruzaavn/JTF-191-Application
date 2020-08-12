<template>
  <v-container fluid>
    <v-row align-content="start">
      <v-col>
        <v-card class="py-4" tile>
          <v-img :src="squadron.img" contain height="500">
            <v-card-title>{{ squadron.name}}</v-card-title>
                    <v-card-subtitle>
                        {{squadron.designation}}<br>
                        Active Pilots {{members.filter(member => member.status === 'active').length}}
                    </v-card-subtitle>
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
                  <h4>Flight Hours</h4>
                  <v-simple-table dense>
                    <thead>
                      <th>Airframe</th>
                      <th>Hours</th>
                    </thead>
                    <tbody>
                      <tr
                        v-for="(hours, airframe) in member.stats.hours"
                        :key="airframe"
                      >
                        <td>{{ airframe }}</td>
                        <td>{{ hours.toPrecision(1) }}</td>
                      </tr>
                    </tbody>
                  </v-simple-table>
                </v-col>
                <v-col>
                  <h4>Kills</h4>
                  <v-simple-table dense>
                    <thead>
                      <th>Victim</th>
                      <th>Number</th>
                    </thead>
                    <tbody>
                      <tr
                        v-for="(kills, victims) in member.stats.kills"
                        :key="victims"
                      >
                        <td>{{ victims }}</td>
                        <td>{{ kills }}</td>
                      </tr>
                    </tbody>
                  </v-simple-table>
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
}
</script>

<style></style>

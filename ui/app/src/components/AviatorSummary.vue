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
        <v-container>
          <v-row id="ribbon-rack" align="center" justify="center">
            <v-col
              cols="4"
              align="center"
              v-for="citations in aviator.citations"
              :key="citations.id"
              class="pa-0"
            >
              <v-img :src="citations.award.ribbon_image" />
            </v-col>
          </v-row>
        </v-container>
      </v-col>
    </v-row>
    <v-card-text>
      <v-row>
        <v-col>
          <h4>Total Flight Hours {{ totalFlightHours }}</h4>
          <v-table
            dense
            :headers="hoursHeaders"
            :items="toHoursTable(aviatorAggregatedFlightStats)"
          >
          </v-table>
        </v-col>
        <v-col>
          <h4>Total kills {{ totalKills }}</h4>
          <v-table
            dense
            :hide-default-footer="true"
            :headers="killsHeaders"
            :items="toKillsTable(aviatorAggregatedCombatStats)"
          >
            <template v-slot:[`item.target`]="{ item }">
              <!-- fixme eslint Vue3 error dont really know why i have to put it in brackets to make it happy, found on stack overflow -->
              <v-icon v-if="item.target === 'air'">fa-fighter-jet fa-xs</v-icon>
              <v-icon v-if="item.target === 'maritime'">fa-ship fa-xs</v-icon>
              <v-icon v-if="item.target === 'ground'">mdi-tank</v-icon>
            </template>
          </v-table>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6">
          <h4>Flight frequency last 90 days</h4>
          <GChart type="LineChart" @ready="getAviatorTimeSeriesStats" />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import moment from "moment";
import axios from "axios";
import { GChart } from "vue-google-charts";

export default {
  name: "AviatorSummary",

  props: {
    aviator: {
      type: Object,
      required: true,
    },
  },
  components: {
    GChart,
  },
  data: () => ({
    ranks: {
      "-4": "https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw1.svg",
      "-3": "https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw2.svg",
      "-2": "https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw3.svg",
      "-1": "https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw4.svg",
      0: "https://www.army.mil/e2/images/rv7/ranks/badges/warrant_officer/sm/cw5.svg",
      1: "https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/second_lieutenant.svg",
      2: "https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/first_lieutenant.svg",
      3: "https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/captain.svg",
      4: "https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/major.svg",
      5: "https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/lieutenant_colonel.svg",
      6: "https://www.army.mil/e2/images/rv7/ranks/badges/officer/sm/colonel.svg",
    },
    hoursHeaders: [
      {
        text: "Airframe",
        align: "start",
        sortable: true,
        value: "airframe",
      },
      { text: "Hours", sortable: true, align: "start", value: "hours" },
    ],
    killsHeaders: [
      {
        text: "Target",
        align: "start",
        sortable: true,
        value: "target",
      },
      { text: "Number", sortable: true, align: "start", value: "number" },
    ],
    aviatorAggregatedFlightStats: [],
    aviatorAggregatedCombatStats: [],
    aviatorTimeSeriesStats: [],
    totalFlightHours: 0,
    totalKills: 0,
  }),
  mounted() {
    this.getAviatorAggregatedFlightStats(this.aviator.id);
    this.getAviatorAggregatedCombatStats(this.aviator.id);
  },
  filters: {
    upper: function (value) {
      return value.toUpperCase();
    },
  },
  methods: {
    updateTotalFlightHours(stats) {
      let totalDurations = moment.duration("0");
      for (const stat in stats) {
        totalDurations.add(moment.duration(stats[stat].total_flight_time));
      }

      this.totalFlightHours = totalDurations.asHours().toFixed(2);
    },
    updateTotalKills(stats) {
      this.totalKills = stats.reduce(
        (cur, prev) => {
          return { kills: prev.kills + cur.kills };
        },
        { kills: 0 }
      ).kills;
    },
    toHoursTable(stats) {
      let data = [];

      for (const stat in stats) {
        const hours = moment
          .duration(stats[stat].total_flight_time)
          .asHours()
          .toFixed(2);
        data.push({ airframe: stats[stat].platform, hours: hours });
      }
      return data;
    },
    toKillsTable(kills) {
      let data = [];
      kills.reduce(function (res, value) {
        if (!res[value.type]) {
          res[value.type] = {
            number: 0,
            target: value.type,
          };
          data.push(res[value.type]);
        }
        res[value.type].number += value.kills;
        return res;
      }, {});
      return data;
    },
    getAviatorAggregatedFlightStats(aviatorId) {
      const token = localStorage.getItem("token");
      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };
      axios
        .get(`/api/roster/stats/flightlog/aggregate/${aviatorId}/`, {}, config)
        .then((response) => {
          this.aviatorAggregatedFlightStats = response.data;
          this.updateTotalFlightHours(response.data);
        });
    },
    getAviatorAggregatedCombatStats(aviatorId) {
      const token = localStorage.getItem("token");
      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };
      axios
        .get(`/api/roster/stats/combatlog/aggregate/${aviatorId}/`, {}, config)
        .then((response) => {
          this.aviatorAggregatedCombatStats = response.data;
          this.updateTotalKills(response.data);
        });
    },
    getAviatorTimeSeriesStats(chart, google) {
      const token = localStorage.getItem("token");
      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };
      axios
        .get(
          `/api/roster/stats/flightlog/timeseries/${this.aviator.id}/90/`,
          {},
          config
        )
        .then((response) => {
          this.aviatorTimeSeriesStats.push(["Date", "Hours"]);
          if (response.data.length > 0) {
            const today = moment();
            let startDate = moment().subtract(90, "days");
            // console.log(startDate)
            for (const stat in response.data) {
              // fill in the gaps in dates with 0s
              const currentStat = response.data[stat];
              const currentDate = moment(currentStat.date);
              if (currentDate.isAfter(startDate)) {
                for (
                  const m = startDate;
                  m.isBefore(currentStat.date);
                  m.add(1, "days")
                ) {
                  this.aviatorTimeSeriesStats.push([m.format("YYYY-MM-DD"), 0]);
                }
              }
              const hours = moment
                .duration(currentStat.total_flight_time)
                .asHours()
                .toFixed(2);
              this.aviatorTimeSeriesStats.push([
                currentStat.date,
                parseFloat(hours),
              ]);
              startDate = currentDate.add(1, "days");
            }

            // fill in up to today is necessary
            if (today.isAfter(startDate)) {
              for (const m = startDate; m.isBefore(today); m.add(1, "days")) {
                this.aviatorTimeSeriesStats.push([m.format("YYYY-MM-DD"), 0]);
              }
            }
          } else {
            this.aviatorTimeSeriesStats.push(["", 0]);
          }
          const chartOptions = {
            legend: { position: "none" },
            chartArea: { width: "90%", height: "80%" },
            titlePosition: "none",
          };
          chart.draw(
            google.visualization.arrayToDataTable(this.aviatorTimeSeriesStats),
            chartOptions
          );
        });
    },
  },
};
</script>

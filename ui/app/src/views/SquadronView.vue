<template>
  <v-container style="min-height: 100vh">
    <v-row align-content="start">
      <v-col>
        <v-card class="py-4" tile>
          <v-img :src="squadron.img" contain height="500"> </v-img>
          <v-card-title>
            Name: {{ squadron.name }} <br />
            Tricode: {{ squadron.tri_code }} <br />
            Designation: {{ squadron.designation }} <br />
            Aircraft: {{ squadron.air_frame.name }} <br />
            Callsign: {{ squadron.callsign.toUpperCase() }} <br />
            Aviators: {{ members.length }}
          </v-card-title>
          <v-card class="mx-4 my-5 py-2">
            <MarkdownComponent
              class="px-2"
              :content="squadron.description"
            ></MarkdownComponent>
          </v-card>
          <div v-for="member in members" :key="member.id">
            <AviatorSummary :aviator="member" />
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import AviatorSummary from "../components/AviatorSummary.vue";
import MarkdownComponent from "../components/MarkdownComponent.vue";

export default {
  name: "SquadronView",
  components: {
    MarkdownComponent,
    AviatorSummary,
  },
  props: ["squadronDesignation"],
  data: () => ({}),
  computed: {
    ...mapGetters(["roster", "squadrons"]),
    members: function () {
      return this.roster.filter(
        (pilot) => pilot.squadron.designation === this.squadronDesignation
      );
    },
    squadron: function () {
      return this.squadrons.filter(
        (sqd) => sqd.designation === this.squadronDesignation
      )[0];
    },
  },
  methods: {
    ...mapActions(["getSquadrons", "getRoster", "getHQs"]),
  },
  mounted() {
    this.getHQs();
    this.getSquadrons();
    this.getRoster();
  },
};
</script>

<style></style>

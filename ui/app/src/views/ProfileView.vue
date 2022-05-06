<template>
  <v-container style="min-height: 100vh">
    <v-row class="pb-10">
      <v-col v-if="aviator.squadron" align="center">
        <img
          :src="aviator.squadron.img"
          style="max-height: 30vh; text-align: center"
          :alt="aviator.squadron.name"
        />
      </v-col>
    </v-row>
    <AviatorSummary :aviator="aviator" v-if="aviator.id" />
    <DynamicLiveries />
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import AviatorSummary from "../components/AviatorSummary.vue";
import DynamicLiveries from "../components/DynamicLiveries.vue";

export default {
  name: "ProfileView",
  components: {
    AviatorSummary,
    DynamicLiveries,
  },
  data: () => ({
    tab: null,
    tabs_sections: ["Stats", "Actions", "Training"],
  }),
  methods: {
    ...mapActions(["getAviatorFromUser", "getUser"]),
  },
  computed: {
    ...mapGetters(["aviator", "user"]),
  },
  mounted() {
    this.getUser()
      .then(() => {
        this.getAviatorFromUser(this.user.id);
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>

<style></style>

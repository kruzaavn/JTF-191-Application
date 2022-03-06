<template>
  <v-container>
    <v-row
      align-content="start"
      v-for="(squadron_type, index) in squadron_types"
      :key="index"
    >
      <v-container>
        <v-row>
          <h1>
            {{ squadron_type[0].toUpperCase() + squadron_type.slice(1) }}
            Squadrons
          </h1>
        </v-row>
        <v-row>
          <v-col
            v-for="squadron in squadrons.filter(
              (x) => x.type === squadron_type
            )"
            :key="squadron.id"
            md="4"
            lg="3"
            sm="12"
            class="d-flex child-flex"
          >
            <v-card
              :to="'/squadron/' + squadron.designation"
              dark
              color="grey"
              class="mx-auto"
              tile
            >
              <v-img
                contain
                :src="squadron.img"
                height="30vh"
                class="my-1"
              ></v-img>
              <div class="description-card mt-auto">
                <v-card-title>
                  {{ squadron.name }}
                </v-card-title>
                <v-card-subtitle>
                  {{ squadron.designation }}
                </v-card-subtitle>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "SquadronList",
  components: {},
  data: () => ({
    local: location.host,
  }),
  methods: {
    ...mapActions([]),
  },
  computed: {
    ...mapGetters(["squadrons"]),
    squadron_types: function () {
      // this function returns a unique set of squadron types returned by the api at /api/roster/squadrons/list/

      let squadron_types = this.squadrons.map((squadron) => squadron.type);
      return [...new Set(squadron_types)];
    },
  },
};
</script>

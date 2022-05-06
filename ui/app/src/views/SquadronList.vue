<template>
  <v-container style="min-height: 100vh">
    <v-row
      align-content="start"
      v-for="(squadron_type, index) in squadron_types"
      :key="index"
    >
      <v-col>
        <v-row>
          <v-col>
            <h1>
              {{ squadron_type[0].toUpperCase() + squadron_type.slice(1) }}
              Squadrons
            </h1>
          </v-col>
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
            <v-container>
              <v-row>
                <v-col>
                  <v-card
                    :to="'/squadron/' + squadron.designation"
                    class="mx-auto"
                    tile
                  >
                    <v-img
                      :src="squadron.img"
                      min-height="33vh"
                      aspect-ratio="16:9"
                    >
                    </v-img>
                    <v-divider></v-divider>
                    <v-card-title>
                      {{ squadron.name }}
                    </v-card-title>

                    <v-card-text>
                      {{ squadron.designation }}
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-col>
        </v-row>
      </v-col>
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
    ...mapActions(["getSquadrons"]),
  },
  computed: {
    ...mapGetters(["squadrons"]),
    squadron_types: function () {
      // this function returns a unique set of squadron types returned by the api at /api/roster/squadrons/list/

      let squadron_types = this.squadrons.map((squadron) => squadron.type);
      return [...new Set(squadron_types)];
    },
  },
  mounted() {
    this.getSquadrons();
  },
};
</script>

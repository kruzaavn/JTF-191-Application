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
            cols="3"
          >
            <v-card
              width="450"
              class="my-4 mx-4 py-2 px-2"
              :to="'/squadron/' + squadron.designation"
              dark
              color="#00000077"
              tile
            >
              <v-img
                contain
                position="center"
                max-height="300px"
                height="300px"
                class="mx-1 my-2"
                :src="squadron.img"
              >
              </v-img>
              <v-divider></v-divider>
              <v-card-title>
                {{ squadron.name }}
              </v-card-title>
              <v-card-subtitle>
                {{ squadron.designation }}
              </v-card-subtitle>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'Home',
  components: {},
  data: () => ({
    local: location.host,
  }),
  methods: {
    ...mapActions([]),
  },
  computed: {
    ...mapGetters(['squadrons']),
    squadron_types: function () {
      // this function returns a unique set of squadron types returned by the api at /api/roster/squadrons/list/

      let squadron_types = this.squadrons.map((squadron) => squadron.type)
      return [...new Set(squadron_types)]
    },
  },
}
</script>

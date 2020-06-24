<template>
    <v-container fluid>

            <v-layout
                    row
                    wrap
            >
                <v-flex
                        v-for="squadron in squadrons"
                        :key="squadron.id"
                >
                    <v-card
                        max-width="450"
                    >
                        <v-img
                                class="align-end"
                                width="450px"
                                :src="squadron.img"
                        >
                            <v-card-title>
                                {{squadron.name}}
                            </v-card-title>
                        </v-img>
                        <v-card-subtitle>
                            {{squadron.designation}}
                        </v-card-subtitle>
                    </v-card>
                </v-flex>
            </v-layout>

    </v-container>
</template>

<script>
// @ is an alias to /src

import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Home',
  components: {
  },
    data: () => ({
      local: location.host,
    }),
  methods: {
      ...mapActions([]),

  },
  computed: {
      ...mapGetters(['squadrons']),

  }
}
</script>

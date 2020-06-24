<template>
    <v-container >

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
                        class="my-4"
                        :to="'/squadron/' + squadron.designation"
                    >
                        <v-img
                                contain
                                position="center"
                                max-height="300px"
                                :src="squadron.img"
                        >
                        </v-img>
                        <v-card-title>
                            {{squadron.name}}
                        </v-card-title>
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

<template>
    <v-container >

            <v-row


            >
                <v-col
                        v-for="squadron in squadrons"
                        :key="squadron.id"
                        cols="3"
                >
                    <v-card
                        max-width="450"
                        class="my-4 mx-4"
                        :to="'/squadron/' + squadron.designation"
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
                        <v-card-title>
                            {{squadron.name}}
                        </v-card-title>
                        <v-card-subtitle>
                            {{squadron.designation}}
                        </v-card-subtitle>
                    </v-card>
                </v-col>
            </v-row>

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

<template>
  <v-container fluid>
    <v-row>
      <v-col cols="2">
      Big Hairy Balls!
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "Tracker",
  data: () => ({
        munitionsHeader: [
        {
          text: 'Stores',
          align: 'start',
          sortable: true,
          value: 'munition',
        },
        {text: 'Munition', value: 'munition'},
        {text: 'Count', value: 'count'},
        {text: 'Category', value: 'type'},
      ],
      }
    ),
  methods: {
    ...mapActions(['getMunitionsList','getStoresList','getOperationList'])

  },

  computed: {
    ...mapGetters(['munitions', 'stores', 'operation']),

  },
  mounted() {
    this.getMunitionsList();
    this.getStoresList();
    this.getOperationList()
  }
}
</script>

<style scoped>

</style>
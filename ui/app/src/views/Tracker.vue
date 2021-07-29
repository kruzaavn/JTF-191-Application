<template>
  <v-container fluid>
    <v-row>
      <v-col>
        Big Harry Ballz!
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-data-table
          :headers="munitionsHeader"
          :items="munitionsTable"
          item-key="name"
          group-by="squadron_name"
          class="elevation-1"
          >
        </v-data-table>
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
          {text: 'Squadron', value: 'squadron_name'},
          {text: 'Munition', value:'munition_name'},
          {text: 'Count', value:'count'},
          {text: 'Category', value: 'munition_type'},
        ],

      }
  ),


  computed: {
    ...mapGetters(['munitions', 'stores','munitionsTable']),

    // eslint-disable-next-line vue/return-in-computed-property
    mounted() {
      this.getMunitionsList();
      this.getStoresList();
    },
  },

  methods: {
    ...mapActions(['getMunitionsList', 'getStoresList']),
  },
  }

</script>

<style scoped>

</style>



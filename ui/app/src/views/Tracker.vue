<template>
  <v-container fluid>
    <v-row>
      <v-col cols="2">
        Big Hairy Balls!
      </v-col>
      <v-data-table
          dense
          :headers="munitionsHeader"
          :items="toMunitionsTable(stores)"
          item-key="name"
          class="elevation-1"
      ></v-data-table>
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
            value: 'type',
          },
          {text: 'Munition', value:'munition'},
          {text: 'Count', value:'count'},
          {text: 'Category', value: 'munitionType'},
        ],

      }
  ),


  computed: {
    ...mapGetters(['munitions', 'stores']),

    // eslint-disable-next-line vue/return-in-computed-property
    mounted() {
      this.getMunitionsList();
      this.getStoresList();
    },
  },

  methods: {
    ...mapActions(['getMunitionsList', 'getStoresList']),

    toMunitionsTable(stores) {

      var munitionsObj = stores.reduce(function (acc, arsenal) {

        return {...acc, [arsenal.type]: arsenal}
      }, {})

      var finalCount = munitionsObj

      for (var i=0; i<8; i++) {
        finalCount[stores[i].type].count += stores[i].count
      }

      return finalCount
    }
  },
}

</script>

<style scoped>

</style>



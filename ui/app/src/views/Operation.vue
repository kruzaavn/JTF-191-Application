<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="py-4" tile>
          <v-img v-if="operation" :src="operation.img" contain height="30vh"> </v-img>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <h1>Current Stores</h1>
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
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'Operation',
  props: ['operationName'],
  data: () => ({
    munitionsHeader: [
      { text: 'Squadron', value: 'squadron_name' },
      { text: 'Munition', value: 'munition_name' },
      { text: 'Count', value: 'count' },
      { text: 'Category', value: 'munition_type' },
    ],
  }),
  computed: {
    ...mapGetters(['operations', 'munitionsTable']),
    operation: function () {
        return this.operations.find((op) => op.name === this.operationName)
    },
  },
  methods: {
    ...mapActions(['getOperations', 'getMunitionsList', 'getStoresList']),
  },
  mounted() {
    this.getOperations()
    this.getMunitionsList()
    this.getStoresList(this.operationName)
  },
}
</script>

<style></style>

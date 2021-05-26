<template>
  <v-container fluid>
    <v-row>
      <v-col cols="2">
        <v-img
            max-height="150"
            contain
            src= "{{operation.img}}"
        >
        </v-img>
      </v-col>
    </v-row>
    <v-row align-content= 'start'>
      <v-col>
        <v-card-title>
          Operation: {{operation.name}}
          Start Date: {{operation.start}}
        </v-card-title>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card-title>
          Theater Stores
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col>
              <h4>
                Stores
              </h4>
              <v-data-table
                  :headers="munitionsHeader"
                  :items="toMunitionsTable(storesCount)"
                  group-by="type"
              >
              </v-data-table>
            </v-col>
          </v-row>
        </v-card-text>
      </v-col>
    </v-row>
  </v-container>

</template>
<script>
import { mapGetters } from 'vuex'
export default {
  data: () => {
     type:
      1: 'Bombs',
      2: 'Air to Ground Missiles',
      3: 'Air to Air Missiles',
      4: 'Rockets',
    },
    return {
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
    },
  };

  computed: {
    ...mapGetters(['operation', 'stores']),

  },
}
</script> 
<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="py-4" tile>
          <v-img v-if="operation" :src="operation.img" contain height="30vh">
          </v-img>
          <v-card-title>
            {{ operation.start }} - {{ operation.complete }}
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <h1>Operation Notes</h1>
        <v-card>
          <markdown-it-vue
            class="px-2 py-2"
            :content="operation.notes"
          ></markdown-it-vue>
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
        <v-card>
          <v-card-title>
            <v-row>
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Search"
                hide-details
              >
              </v-text-field>
              <v-spacer></v-spacer>
              <v-select
                :items="groups"
                label="Group By"
                clearable
                v-model="groupby"
              >
              </v-select>
            </v-row>
          </v-card-title>
          <v-data-table
            :headers="munitionsHeader"
            :items="munitionsTable"
            :group-by="groupby"
            item-key="name"
            dense
            multi-sort
            :search="search"
            items-per-page="-1"
          >
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "OperationView",
  props: ["operationName"],
  data: () => ({
    search: "",
    groupby: "squadron_name",
    groups: [
      { text: "Squadron", value: "squadron_name" },
      { text: "Munition", value: "munition_name" },
      { text: "Category", value: "munition_type" },
    ],
    munitionsHeader: [
      { text: "Squadron", value: "squadron_name" },
      { text: "Munition", value: "munition_name" },
      { text: "Count", value: "count", filterable: false, groupable: false },
      { text: "Category", value: "munition_type" },
    ],
  }),
  computed: {
    ...mapGetters(["operations", "munitionsTable"]),
    operation: function () {
      return this.operations.find((op) => op.name === this.operationName);
    },
  },
  methods: {
    ...mapActions(["getOperations", "getMunitionsList", "getStoresList"]),
  },
  mounted() {
    this.getOperations();
    this.getMunitionsList();
    this.getStoresList(this.operationName);
  },
};
</script>

<style></style>

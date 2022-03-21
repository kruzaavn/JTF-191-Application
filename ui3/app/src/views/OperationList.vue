<template>
  <v-container style="min-height: 100vh">
    <v-row>
      <v-col>
        <h1>Operations</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        v-for="operation in operations"
        :key="operation.id"
        md="4"
        lg="3"
        sm="12"
        class="d-flex child-flex"
      >
        <v-card
          :to="'/operation/' + operation.name"
          dark
          tile
          class="mx-auto"
          color="grey"
        >
          <v-img
            :src="operation.img"
            lazy-src="https://dummyimage.com/600x400/bfbfbf/bfbfbf.png"
            height="30vh"
            class="my-1"
            contain
          >
          </v-img>
          <div class="description-card">
            <v-card-title>
              {{ operation.name }}
            </v-card-title>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "OperationList",
  computed: {
    ...mapGetters(["operations"]),
  },
};
</script>

<style></style>

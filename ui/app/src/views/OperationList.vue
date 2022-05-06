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
        <v-container>
          <v-row>
            <v-col>
              <v-card :to="'/operation/' + operation.name" tile>
                <v-img
                  :src="operation.img"
                  lazy-src="https://dummyimage.com/600x400/bfbfbf/bfbfbf.png"
                  min-height="33vh"
                  aspect-ratio="16:9"
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
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "OperationList",
  computed: {
    ...mapGetters(["operations"]),
  },
  methods: {
    ...mapActions(["getOperations"]),
  },
  mounted() {
    this.getOperations();
  },
};
</script>

<style></style>

<template>
  <v-row>
    <v-col>
        <div
          v-for="(doc, docIndex) in filtered_docs"
          :key="docIndex"
        ><h3>{{doc.name}}</h3>
          <v-expansion-panels>

          </v-expansion-panels>
        </div>
    </v-col>
  </v-row>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "DocumentationView",
  components: {},
  props: ["type"],
  computed: {
    ...mapGetters(["documentation"]),
    filtered_docs: function () {
      return this.documentation.filter((doc) => doc.type === this.type);
    },
  },
  methods: {
    ...mapActions(["getDocumentation", "getDocumentationModules"]),
  },
  mounted() {
    this.getDocumentation();
    this.getDocumentationModules();
  },
};
</script>

<style scoped></style>

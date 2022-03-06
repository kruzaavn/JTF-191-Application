<template>
  <DocumentationViewer
    title="Training Qualifications"
    :docs="filtered_docs"
  ></DocumentationViewer>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import DocumentationViewer from "../components/DocumentationViewer";

export default {
  name: "QualificationView",
  components: { DocumentationViewer },
  props: ["qualificationModule"],
  computed: {
    ...mapGetters(["documentation"]),
    filtered_docs: function () {
      return this.documentation.filter((doc) => (doc.type = "training"));
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

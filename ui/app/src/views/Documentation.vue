<template>
  <DocumentationViewer title="Documentation" :docs="filtered_docs"></DocumentationViewer>
</template>

<script>
import DocumentationViewer from "../components/DocumentationViewer";
import {mapActions, mapGetters} from "vuex";

export default {
  name: "Documentation",
  components: {DocumentationViewer},
  computed: {
    ...mapGetters(['documentation']),
    filtered_docs: function () {
      return this.documentation.filter(doc => doc.type = 'admin')
    }
  },
  methods: {
    ...mapActions(['getDocumentation', 'getDocumentationModules']),
  },
  mounted() {
      this.getDocumentation()
      this.getDocumentationModules()
  },

}
</script>

<style scoped>

</style>
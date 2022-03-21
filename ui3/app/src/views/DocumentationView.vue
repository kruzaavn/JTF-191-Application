<template>
  <v-container style="height: 100vh">
    <v-row>
      <v-col>
        <h1>{{ pageName }}</h1>
        <div v-for="(doc, docIndex) in filtered_docs" :key="docIndex">
          <h2>{{ doc.name }}</h2>
          <v-expansion-panels>
            <v-expansion-panel
              v-for="(docModule, docModuleIndex) in get_modules(doc.modules)"
              :key="docModuleIndex"
            >
              <v-expansion-panel-title>
                <template v-slot:default="{ expanded }">
                  <v-row>
                    <v-col class="d-flex justify-start">
                      {{ docModule.name }}
                    </v-col>
                    <v-col class="d-flex justify-end text-grey">
                      <v-fade-transition leave-absolute>
                        <span v-if="expanded" key="0"> Close </span>
                        <span v-else key="1"></span>
                      </v-fade-transition>
                    </v-col>
                  </v-row>
                </template>
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <iframe
                  :src="setIframeLink(docModule)"
                  width="100%"
                  :height="iframeHeight"
                  @load="setIframeHeight"
                >
                </iframe>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "DocumentationView",
  components: {},
  props: ["type", "pageName"],
  data() {
    return {
      iframeHeight: 0,
    };
  },
  computed: {
    ...mapGetters(["documentation", "documentationModules"]),
    filtered_docs: function () {
      return this.documentation.filter((doc) => doc.type === this.type);
    },
  },
  methods: {
    ...mapActions(["getDocumentation", "getDocumentationModules"]),
    get_modules: function (module_list) {
      return this.documentationModules.filter((module) =>
        module_list.includes(module.id)
      );
    },
    setIframeHeight() {
      this.iframeHeight = window.innerHeight * 0.8;
    },
    setIframeLink(module) {
      if (module.documentation_type === "document") {
        return `${module.link}?embedded=true`;
      } else if (module.documentation_type === "slides") {
        return module.link.replace("/pub", "/embed");
      } else if (module.documentation_type === "spreadsheet") {
        return `${module.link}?widget=true&amp;headers=false`;
      } else if (module.documentation_type === "video") {
        return module.link.replace("watch?v=", "embed/");
      } else {
        return module.link;
      }
    },
  },
  mounted() {
    this.getDocumentation();
    this.getDocumentationModules();
  },
};
</script>

<style scoped>
iframe {
  border: 0;
  min-width: 100%;
}
</style>

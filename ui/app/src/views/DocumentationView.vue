<template>
  <v-container style="min-height: 100vh">
    <v-row>
      <v-col>
        <h1>{{ pageName }}</h1>
        <div v-for="(doc, docIndex) in filtered_docs" :key="docIndex">
          <h2>{{ doc.name }}</h2>
          <MarkdownComponent :content="doc.description"> </MarkdownComponent>
          <v-expansion-panels>
            <v-expansion-panel
              v-for="(docModule, docModuleIndex) in get_modules(doc)"
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
                <IFrameComponent :documentModule="docModule"></IFrameComponent>
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
import IFrameComponent from "../components/IFrameComponent.vue";
import MarkdownComponent from "../components/MarkdownComponent.vue";

export default {
  name: "DocumentationView",
  components: { IFrameComponent, MarkdownComponent },
  props: ["type", "pageName"],
  computed: {
    ...mapGetters(["documentation", "documentationModules"]),
    filtered_docs: function () {
      return this.documentation.filter((doc) => doc.type === this.type);
    },
  },
  methods: {
    ...mapActions(["getDocumentation", "getDocumentationModules"]),
    get_modules: function (documentation) {
      let modules = this.documentationModules.filter((module) =>
        documentation.modules.includes(module.id)
      );

      let orderdModule = documentation.order.sort((a, b) => a.rank - b.rank);

      let orderedModules = [];

      for (let i = 0; i < orderdModule.length; i++) {
        for (let j = 0; j < modules.length; j++) {
          if (modules[j].name === orderdModule[i].module) {
            orderedModules.push(modules[j]);
            modules.splice(j, 1);
          }
        }
      }

      return orderedModules.concat(
        modules.sort(function (a, b) {
          const nameA = a.name.toUpperCase(); // ignore upper and lowercase
          const nameB = b.name.toUpperCase(); // ignore upper and lowercase
          if (nameA < nameB) {
            return -1;
          }
          if (nameA > nameB) {
            return 1;
          }

          // names must be equal
          return 0;
        })
      );
    },
  },
  mounted() {
    this.getDocumentation();
    this.getDocumentationModules();
  },
};
</script>

<style scoped></style>

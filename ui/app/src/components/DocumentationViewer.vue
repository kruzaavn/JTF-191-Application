<template>
  <v-container>
    <v-card v-if="!documentation" min-height="80vh">
      <v-card-title>{{ title }}</v-card-title>
      <v-list>
        <v-list-group
          v-for="qualification in qualifications"
          :key="qualification.id"
        >
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title
                v-text="qualification.name"
              ></v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item
            v-for="(moduleID, index) in qualification.modules"
            :key="index"
          >
            <v-list-item-content>
              <v-list-item-title
                v-if="getQualModule(moduleID)"
                v-text="getQualModule(moduleID).name"
                @click="setDocumentation(moduleID)"
              ></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
      </v-list>
    </v-card>
    <v-card v-if="documentation">
      <v-card-title
        >{{ documentation.name }}
        <v-spacer></v-spacer>
        <v-icon right @click="clearDocumentation">mdi-close</v-icon>
      </v-card-title>

      <iframe
        v-if="documentation"
        id="frame"
        :src="setIframeLink()"
        :height="iframeHeight"
        @load="setIframeHeight()"
      ></iframe>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "DocumentationViewer",
  props: {
    title: String
  }
}
</script>

<style scoped>

</style>
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
import { mapGetters }from "vuex";

export default {
  name: "DocumentationViewer",
  props: {
    title: String,
    docs: Array
  },
  data() {
    return {
      iframeHeight: 0, // initial height
      documentation: null,
    }
  },
  computed: {
    ...mapGetters(['documentationModules'])
  },
  methods: {

    setIframeHeight() {
      if (this.documentation.documentation_type === 'document') {
        this.iframeHeight = 5000
      } else if (
        ['slides', 'spreadsheet', 'video'].includes(
          this.documentation.documentation_type
        )
      ) {
        this.iframeHeight = window.innerHeight * 0.8
      }
    },
    setIframeLink() {
      if (this.documentation.documentation_type === 'document') {
        return `${this.documentation.link}?embedded=true`
      } else if (this.documentation.documentation_type === 'slides') {
        return this.documentation.link.replace('/pub', '/embed')
      } else if (this.documentation.documentation_type === 'spreadsheet') {
        return `${this.documentation.link}?widget=true&amp;headers=false`
      } else if (this.documentation.documentation_type === 'video') {
        return this.documentation.link.replace('watch?v=', 'embed/')
      } else {
        return this.documentation.link
      }
    }
  }
}
</script>

<style scoped>

  iframe {
    border: 0;
    min-width: 100%;
  }

</style>
<template>
  <v-container>
    <v-card v-if="!documentation" min-height="80vh">
      <v-card-title>Quals</v-card-title>
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
import { mapActions, mapGetters } from 'vuex'
import router from '@/router'

export default {
  name: 'Qualification',
  props: ['qualificationModule'],
  data() {
    return {
      iframeHeight: 0, // initial height
      documentation: null,
    }
  },
  computed: {
    ...mapGetters(['qualifications', 'qualificationModules']),
  },
  methods: {
    ...mapActions(['getQualifications', 'getQualificationModules']),
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
    },
    getQualModule(moduleID) {
      return this.qualificationModules.find(
        (qualModule) => qualModule.id === moduleID
      )
    },
    setDocumentation(moduleID) {
      this.documentation = this.getQualModule(moduleID)
      router.push({
        name: 'Qualification',
        params: { qualificationModule: this.documentation.name },
      })
    },
    clearDocumentation() {
      this.documentation = null
      this.qualificationModule = 'list'
      router.push({
        name: 'Qualification',
        params: { qualificationModule: this.qualificationModule },
      })
    },
  },
  mounted() {
    setTimeout(() => {
      this.getQualifications()
    }, 250)
    setTimeout(() => {
      this.getQualificationModules()
    }, 750)
    if (this.qualificationModule !== 'list' && this.qualificationModules) {
      this.documentation = this.qualificationModules.find(
        (qualModule) => qualModule.name === this.qualificationModule
      )
    }
  },
}
</script>

<style scoped>
iframe {
  border: 0;
  min-width: 100%;
}
</style>

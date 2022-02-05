<template>
  <DocumentationViewer title="Training Qualifications"></DocumentationViewer>
</template>

<script>

import { mapActions, mapGetters } from 'vuex'
import router from '@/router'
import DocumentationViewer from "../components/DocumentationViewer";

export default {
  name: 'Qualification',
  components: {DocumentationViewer},
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

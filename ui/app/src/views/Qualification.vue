<template>
  <v-container>
    <div v-if="!documentation">
      <h1>Quals</h1>
      <v-list>
        <v-list-group
            v-for="qualification in qualifications"
            :key="qualification.id"
        >
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title v-text="qualification.name"></v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item
              v-for="(moduleID, index) in qualification.modules"
              :key="index"
          >
            <v-list-item-content>
              <v-list-item-title
                  v-text="qualificationModules.find(qualModule => qualModule.id === moduleID).name"
                  @click="setDocumentation(moduleID)"
              ></v-list-item-title>
            </v-list-item-content>
          </v-list-item>

        </v-list-group>

      </v-list>

    </div>
    <div v-if="documentation">
      <h1>{{documentation.name}}</h1>
      <iframe
          v-if="documentation"
          id="frame"
          :src="documentation.link"
          :height="iframeHeight"
          @load="setIframeHeight('document')"></iframe>
    </div>
  </v-container>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'

export default {
  name: "Qualification",
  props: ['qualificationModule'],
  data() {
    return {
      iframeHeight: 0, // initial height
      documentation: null
    };
  },
  computed: {
    ...mapGetters(['qualifications', 'qualificationModules']),
  },
  methods: {
    ...mapActions(['getQualifications']),
    setIframeHeight(type) {
      if (type === 'document') {
        this.iframeHeight = 5000
      }
    },
    setDocumentation(moduleID) {

      this.documentation =  this.qualificationModules.find(qualModule => qualModule.id === moduleID)

    }
  },
  mounted() {
    this.getQualifications()
  }
}
</script>

<style scoped>
iframe {
  border: 0;
  min-width: 100%;
  background: deeppink;
}
</style>
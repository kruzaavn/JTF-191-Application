<template>
  <v-container>
    <h1>Quals</h1>
    <p v-for="qualification in qualifications" :key="qualification.id">{{qualification.name}}</p>
    <iframe src="https://docs.google.com/document/d/e/2PACX-1vSFHt9eJfYdfqhdoQDIbLHS-Lzvp8l-NV3VCqQeATDdNOGGaVToy8uwgh_43crKO6RUYt3_y-iVrgOj/pub?embedded=true" width="100%" height="100%" style="border: 0"></iframe>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: "Qualification",
  props: ['qualificationModule'],
  computed: {
    ...mapGetters(['qualifications', 'qualificationModules']),
  },
  methods: {
    ...mapActions(['getQualifications']),
  },
    mounted() {
      console.log('loading')
      this.getQualifications()
  },
}
</script>

<style scoped>

</style>
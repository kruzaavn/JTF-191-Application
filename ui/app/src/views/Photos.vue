<template>
  <v-container>
    <v-row>
      <v-col
        v-for="photo in photos"
        :key="photo.key"
        cols="4"
        class="d-flex child-flex"
      >
        <v-lazy>
          <v-img :src="photo.url || photo.file" height="30vh"> </v-img>
        </v-lazy>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
export default {
  name: 'Photos',
  data: () => ({}),
  computed: {
    ...mapGetters(['photos']),
  },
  methods: {
    ...mapActions(['getPhotos']),
  },
  mounted() {
    this.getPhotos()
  },
}
</script>

<style></style>

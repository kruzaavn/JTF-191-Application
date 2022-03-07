<template>
  <v-container
      class=""
  style="height: 100vh;"
  >
    <v-row>
      <v-col
        v-for="photo in photos"
        :key="photo.key"
        md="4"
        lg="3"
        sm="6"
        cols="12"
        class="d-flex child-flex"
      >

          <v-img
            :src="photo.url || photo.file"
            aspect-ratio="16:9"
            lazy-src="https://dummyimage.com/600x400/bfbfbf/bfbfbf.png"
          >
          </v-img>

      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "PhotosView",
  data: () => ({}),
  computed: {
    ...mapGetters(["photos"]),
  },
  methods: {
    ...mapActions(["getPhotos"]),
  },
  mounted() {
    this.getPhotos();
  },
};
</script>

<style>


</style>

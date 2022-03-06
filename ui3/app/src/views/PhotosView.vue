<template>
  <v-container>
    <v-row>
      <v-col
        v-for="photo in photos"
        :key="photo.key"
        md="4"
        lg="3"
        sm="6"
        class="d-flex child-flex"
      >
        <v-lazy>
          <v-img
            :src="photo.url || photo.file"
            height="30vh"
            lazy-src="https://dummyimage.com/600x400/bfbfbf/bfbfbf.png"
          >
          </v-img>
        </v-lazy>
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

<style></style>

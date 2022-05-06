<template>
  <iframe
    :src="setIframeLink(documentModule)"
    width="100%"
    :height="iframeHeight"
    @load="setIframeHeight"
  >
  </iframe>
  <div class="text-center" v-if="loading">
    <v-progress-circular indeterminate size="10vh"></v-progress-circular>
  </div>
</template>

<script>
export default {
  name: "IFrameComponent",
  props: ["documentModule"],
  data() {
    return {
      iframeHeight: 0,
      loading: true,
    };
  },
  methods: {
    setIframeHeight() {
      this.iframeHeight = window.innerHeight * 0.8;
      this.loading = false;
    },
    setIframeLink(module) {
      if (module.documentation_type === "document") {
        return `${module.link}?embedded=true`;
      } else if (module.documentation_type === "slides") {
        return module.link.replace("/pub", "/embed");
      } else if (module.documentation_type === "spreadsheet") {
        return `${module.link}?widget=true&amp;headers=false`;
      } else if (module.documentation_type === "video") {
        return module.link.replace("watch?v=", "embed/");
      } else {
        return module.link;
      }
    },
  },
};
</script>

<style scoped>
iframe {
  border: 0;
  min-width: 100%;
}
</style>

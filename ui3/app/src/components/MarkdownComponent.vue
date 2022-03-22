<template>
  <div class="markdown" v-html="markdownToHtml"></div>
</template>

<script>
import {marked} from "marked";

export default {
  name: "MarkdownComponent",
  props: ["content"],
  computed: {
    markdownToHtml() {
      return marked.parse(this.content);
    },
  },
};
</script>

<style scoped>

</style>

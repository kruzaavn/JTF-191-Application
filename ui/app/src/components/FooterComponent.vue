<template>
  <div class="text-center align-end">
  </div>
</template>

<script>
export default {
  name: "FooterComponent",
  mounted() {
    kofiWidgetOverlay.draw('jtf191', {
      'type': 'floating-chat',
      'floating-chat.donateButton.text': 'Donate',
      'floating-chat.donateButton.background-color': '#00b9fe',
      'floating-chat.donateButton.text-color': '#fff'
    });
  }
};
</script>

<style scoped></style>

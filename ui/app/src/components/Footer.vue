<template>
  <v-footer fixed padless>
    <v-col class="text-caption text-center" cols="12">
      Support the Wing
      <form action="https://www.paypal.com/donate" method="post" target="_top">
        <input type="hidden" name="hosted_button_id" value="BJYS8LWHZPEV6" />
        <input
          type="image"
          src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif"
          border="0"
          name="submit"
          title="PayPal - The safer, easier way to pay online!"
          alt="Donate with PayPal button"
        />
      </form>
    </v-col>
  </v-footer>
</template>

<script>
export default {
  name: 'Footer',
}
</script>

<style scoped></style>

<template>
  <v-container>
    <v-row align-content="center" class="pb-10">
        <v-col>
            <v-img
                contain
                :src="aviator.squadron.img"
                height="30vh"
                class="my-1"
            ></v-img>
        </v-col>
    </v-row>
    <AviatorSummary :aviator="aviator"/>
    <DynamicLiveries />
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import AviatorSummary from '@/components/AviatorSummary'
import DynamicLiveries from '@/components/DynamicLiveries'

export default {
  name: 'Profile',
  components: {
      AviatorSummary,
      DynamicLiveries,
  },
  data: () => ({
    tab: null,
    tabs_sections: [
        "Stats",
        "Actions",
        "Training",
    ]
  }),
  methods: {
    ...mapActions(['getAviatorFromUser', 'getUser']),
  },
  computed: {
    ...mapGetters(['aviator', 'user']),
  },
  mounted() {
    this.getUser().then(() => {
      this.getAviatorFromUser(this.user.id)
    })
    .catch((error) => {
      console.log(error)
    })
  },
}
</script>

<style>

</style>
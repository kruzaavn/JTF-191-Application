<template>
  <v-container>
    <v-row align-content="center" class="pb-10">
        <v-col>
            <v-img
                contain
                src="http://localhost:8000/media/squadrons/blackknights.png"
                height="30vh"
                class="my-1"
            ></v-img>
        </v-col>
    </v-row>
    <AviatorSummary :aviator="aviator"/>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import AviatorSummary from '@/components/AviatorSummary'

export default {
  name: 'Profile',
  components: {
      AviatorSummary,
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
    ...mapActions(['getAviator']),
  },
  computed: {
    ...mapGetters(['aviator', 'user']),
  },
  mounted() {
    this.getAviator(this.user.id)
  },
}
</script>

<style>

</style>
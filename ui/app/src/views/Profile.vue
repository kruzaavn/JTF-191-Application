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
    <LeaveOfAbsence :aviator="aviator"/>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import AviatorSummary from '@/components/AviatorSummary'
import LeaveOfAbsence from '@/components/LeaveOfAbsence'

export default {
  name: 'Profile',
  components: {
      AviatorSummary,
      LeaveOfAbsence,
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
    let unsubscribe = this.$store.subscribe(({ type }) => {
      if (type === 'setUser') {
        this.getAviator(this.user.id)
        unsubscribe() // So it only reacts once.
      }
    })
  },
}
</script>

<style>

</style>
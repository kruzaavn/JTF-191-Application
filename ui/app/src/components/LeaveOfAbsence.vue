<template>
  <v-card class="mx-4 my-5 py-2" tile>
    <v-row>
      <v-card-title><v-col>Leave of absence</v-col></v-card-title>
      <v-card-text>
        <v-col>
          <v-data-table
            dense
            :headers="loaHeaders"
            :items="toLOATable(leavesOfAbsence)"
          >
            <template v-slot:[`item.start`]="{ item }">
              <span>{{ new Date(item.start).toDateString() }}</span>
            </template>
            <template v-slot:[`item.end`]="{ item }">
              <span>{{ new Date(item.end).toDateString() }}</span>
            </template>
            <template v-slot:[`item.actions`]="{ item }">
              <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
            </template>
          </v-data-table>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="text-h5"
                >Are you sure you want to delete this LOA?</v-card-title
              >
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDelete"
                  >Cancel</v-btn
                >
                <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                  >Delete</v-btn
                >
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-col>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-col><v-btn @click="newLoa">New LOA</v-btn></v-col>
      </v-card-actions>
      <v-dialog v-model="dialogNewLoa" max-width="500px">
        <v-card>
          <v-card-title class="text-h5">Enter your LOA below</v-card-title>
          <v-card-text>
            <template>
              <v-layout row wrap>
                <v-menu
                  v-model="fromDateMenu"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      label="From Date"
                      prepend-icon="event"
                      readonly
                      :value="fromDateDisp"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    locale="en-in"
                    v-model="newLoaFromDate"
                    no-title
                    @input="fromDateMenu = false"
                  ></v-date-picker>
                </v-menu>
              </v-layout>
            </template>
            <template>
              <v-layout row wrap>
                <v-menu
                  v-model="toDateMenu"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      label="To Date"
                      prepend-icon="event"
                      readonly
                      :value="toDateDisp"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    locale="en-in"
                    v-model="newLoaToDate"
                    no-title
                    @input="toDateMenu = false"
                  ></v-date-picker>
                </v-menu>
              </v-layout>
            </template>
            <template>
              <v-text-field
                label="Description"
                solo
                v-model="newLoaDescription"
              ></v-text-field>
            </template>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="closeNewLoa"
              >Cancel</v-btn
            >
            <v-btn color="blue darken-1" text @click="newLoaConfirm"
              >Submit</v-btn
            >
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </v-card>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'LeaveOfAbsence',
  props: {
      aviator: {
          type: Object,
          required: true
      }
  },
  data: () => ({
    dialogDelete: false,
    dialogNewLoa: false,
    newLoaFromDate: null,
    newLoaDescription: '',
    fromDateMenu: false,
    toDateMenu: false,
    newLoaToDate: null,
    loaOpenIdx: -1,
    loaHeaders: [
      { text: 'ID', sortable: true, align: 'start', value: 'id' },
      { text: 'Start', sortable: true, align: 'start', value: 'start' },
      { text: 'End', sortable: true, align: 'start', value: 'end' },
      { text: 'Description', sortable: false, align: 'start', value: 'description' },
      { text: 'Actions', value: 'actions', sortable: false },
    ]
  }),
  methods: {
    ...mapActions(['deleteLeaveOfAbsence']),
    toLOATable(leavesOfAbsence) {
      let data = []

      for (const loaIDX in leavesOfAbsence) {
        let loa = leavesOfAbsence[loaIDX]
        data.push({
          id: loa.id,
          start: loa.start,
          end: loa.end,
          description: loa.description
        })
      }
      return data
    },
    deleteItem (item) {
      this.loaOpenIdx = item.id
      this.dialogDelete = true
    },
    newLoa() {
      this.dialogNewLoa = true
    },
    deleteItemConfirm () {
      // Call api to delete item with the selected IDX
      this.$store.dispatch('deleteLeaveOfAbsence', {
        aviatorId: this.aviator.id,
        loaId: this.loaOpenIdx
      })
      this.updateLoaSection()
      this.closeDelete()
    },
    newLoaConfirm () {
      if (this.newLoaFromDate && this.newLoaToDate) {
        this.$store.dispatch('createNewLeaveOfAbsence', {
          aviatorId: this.aviator.id,      
          startDate: this.newLoaFromDate,
          endDate: this.newLoaToDate,
          description: this.newLoaDescription,
        })
      }
      this.updateLoaSection()
      this.closeNewLoa()
    },
    closeDelete () {
      this.dialogDelete = false

      // Reset the temp state on next DOM cycle
      this.$nextTick(() => {
        this.loaOpenIdx = -1
      })
    },
    closeNewLoa () {
      this.dialogNewLoa = false
    },
    updateLoaSection() {
      this.$store.dispatch('getLeaveOfAbsence', {
        aviatorId: this.aviator.id
      })
    }
  },
  computed: {
    ...mapGetters(['leavesOfAbsence']),
    fromDateDisp() {
      return this.newLoaFromDate;
    },
    toDateDisp() {
      return this.newLoaToDate;
    },
  },
  watch: {
    dialogDelete (val) {
      val || this.closeDelete()
    },
  },
  mounted() {
    this.updateLoaSection()
  },
}
</script>

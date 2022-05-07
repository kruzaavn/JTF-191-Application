<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>JTF Schedule</h1>
        <FullCalendar
          ref="fullCalendar"
          class="calendar"
          :options="calendarOptions"
        >
        </FullCalendar>
        <v-dialog v-model="dialog">
          <EventComponent
            :event="selectedEvent"
            @dialogClose="calendarUpdate"
          ></EventComponent>
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import "@fullcalendar/core/vdom";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import listPlugin from "@fullcalendar/list";
import rrulePlugin from "@fullcalendar/rrule";
import EventComponent from "../components/EventComponent.vue";
import { mapActions } from "vuex";
import { eventSources } from "../assets/js/eventSources";

export default {
  name: "ScheduleView",
  components: { FullCalendar, EventComponent },
  data: function () {
    return {
      dialog: false,
      selectedEvent: {},
      calendarOptions: {
        plugins: [
          rrulePlugin,
          dayGridPlugin,
          timeGridPlugin,
          listPlugin,
          interactionPlugin,
        ],
        initialView: "listWeek",
        headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "listWeek,timeGridWeek,dayGridMonth",
        },
        selectable: true,
        selectMirror: true,
        nowIndicator: true,
        dayMaxEvents: 3,
        eventClick: this.handleEventClick,
        select: this.handleDateSelect,
        eventMouseEnter: this.handleEnterEvent,
        eventMouseLeave: this.handleLeaveEvent,
        navLinks: true,
        eventSources: eventSources,
      },
    };
  },

  computed: {},
  methods: {
    ...mapActions(["getSquadrons"]),
    handleEventClick: function (clickInfo) {
      this.dialog = !this.dialog;
      this.selectedEvent = clickInfo.event;
    },
    handleDateSelect(selectInfo) {
      let calendarApi = selectInfo.view.calendar;

      calendarApi.unselect(); // clear date selection

      const Event = calendarApi.addEvent({
        title: "NewEvent",
        start: selectInfo.startStr,
        end: selectInfo.endStr,
        backgroundColor: "#F6AE2D",
        textColor: "black",
        editable: true,
        extendedProps: {
          description: "",
        },
      });
    },
    handleEnterEvent(mouseEnterInfo) {
      mouseEnterInfo.event.setProp("borderColor", "red");
    },
    handleLeaveEvent(mouseLeaveInfo) {
      mouseLeaveInfo.event.setProp("borderColor", "");
    },
    calendarUpdate: function () {
      this.dialog = false;
      this.$refs.fullCalendar.getApi().refetchEvents();
    },
  },
  mounted() {
    this.getSquadrons();
  },
};
</script>

<style scoped>
.calendar {
  height: 80vh;
}
</style>

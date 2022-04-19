<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>JTF Schedule</h1>
        <FullCalendar class="calendar" :options="calendarOptions">
        </FullCalendar>
        <v-dialog v-model="dialog">
          <EventComponent
            :event="selectedEvent"
            @dialogClose="this.dialog = false"
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
import EventComponent from "../components/EventComponent.vue";

function formatEvent(eventData) {
  return { title: eventData.name, ...eventData };
}

const eventDefaults = {
  url: "/api/roster/event/list/",
  eventDataTransform: formatEvent,
  editable: true,
};

export default {
  name: "ScheduleView",
  components: { FullCalendar, EventComponent },
  data: function () {
    return {
      dialog: false,
      selectedEvent: {},
      calendarOptions: {
        plugins: [dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin],
        initialView: "dayGridMonth",
        headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek,listMonth",
        },
        selectable: true,
        selectMirror: true,
        nowIndicator: true,
        dayMaxEvents: 3,
        eventClick: this.handleEventClick,
        select: this.handleDateSelect,
        eventMouseEnter: this.handleEnterEvent,
        eventMouseLeave: this.handleLeaveEvent,
        eventSources: [
          {
            extraParams: { type: "operation" },
            backgroundColor: "#F26419",
            textColor: "white",
            ...eventDefaults,
          },
          {
            extraParams: { type: "training" },
            backgroundColor: "#86BBD8",
            textColor: "black",
            ...eventDefaults,
          },
          {
            extraParams: { type: "admin" },
            backgroundColor: "#2F4858",
            textColor: "white",
            ...eventDefaults,
          },
        ],
      },
    };
  },

  computed: {},
  methods: {
    handleEventClick: function (clickInfo) {
      this.dialog = !this.dialog;
      this.selectedEvent = clickInfo.event;
    },
    handleDateSelect(selectInfo) {
      let calendarApi = selectInfo.view.calendar;

      // this.dialog = !this.dialog

      calendarApi.unselect(); // clear date selection

      const Event = calendarApi.addEvent({
        title: "NewEvent",
        start: selectInfo.startStr,
        end: selectInfo.endStr,
        backgroundColor: "#F6AE2D",
        textColor: "black",
        editable: true,
        extendedProps: {
          description: "Enter Event Description",
        },
      });
    },
    handleEnterEvent(mouseEnterInfo) {
      mouseEnterInfo.event.setProp("borderColor", "red");
    },
    handleLeaveEvent(mouseLeaveInfo) {
      mouseLeaveInfo.event.setProp("borderColor", "");
    },
  },
};
</script>

<style scoped>
.calendar {
  height: 80vh;
}
</style>

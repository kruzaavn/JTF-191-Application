<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>JTF Schedule</h1>
        <FullCalendar class="calendar" :options="calendarOptions"
          >
        </FullCalendar>
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
  components: { FullCalendar },
  data: () => ({
    calendarOptions: {
      plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
      initialView: "dayGridMonth",
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,timeGridWeek",
      },
      selectable: true,
      selectMirror: true,
      nowIndicator: true,
      eventSources: [
        {
          extraParams: { type: "operation" },
          color: "blue",
          ...eventDefaults,
        },
        {
          extraParams: { type: "training" },
          color: "green",
          ...eventDefaults,
        },
        {
          extraParams: { type: "admin" },
          color: "purple",
          ...eventDefaults,
        },
      ],
    },
  }),

  computed: {},
  methods: {},
};
</script>

<style scoped>
.calendar {
 height: 80vh;
}
</style>

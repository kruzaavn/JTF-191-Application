<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer expand-on-hover rail position="right">
        <v-list nav>
          <v-list-item
            :prepend-icon="menuPage === 'edit' ? 'mdi-text-box' : 'mdi-xml'"
            :title="menuPage === 'edit' ? 'View' : 'Edit'"
            value="description"
            @click="gotoMenuPage('edit')"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-clock"
            title="Date / Time"
            value="timespan"
            @click="gotoMenuPage('timespan')"
          >
          </v-list-item>
          <v-list-item
            v-if="!event.id"
            prepend-icon="mdi-repeat"
            title="Recurring"
            value="save"
            @click="gotoMenuPage('recurring')"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-content-save"
            title="Save"
            value="save"
            @click="commitEvent"
          ></v-list-item>

          <v-list-item
            class="fixedBottom"
            prepend-icon="mdi-trash-can-outline"
            title="Delete"
            value="delete"
            style="color: red"
            @click="removeEvent"
          ></v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-main class="display-window">
        <div id="menu-page-display" v-if="menuPage === 'display'">
          <v-toolbar :color="getEventBackgroundColor()" class="d-flex"
            ><v-toolbar-title
              :style="{
                color: getEventTextColor(),
              }"
              >{{ title }}</v-toolbar-title
            ></v-toolbar
          >
          <div class="pa-4">
            <h3>
              {{ this.start.toLocaleDateString() }}
              {{ this.start.toLocaleTimeString() }} -
              {{
                this.start.toLocaleDateString() ===
                this.end.toLocaleDateString()
                  ? ""
                  : this.end.toLocaleDateString()
              }}
              {{ this.end.toLocaleTimeString() }}
            </h3>
          </div>
          <MarkdownComponent
            :content="description"
            class="pa-4"
          ></MarkdownComponent>
        </div>
        <div id="menu-page-edit" v-if="menuPage === 'edit'">
          <v-toolbar :color="getEventBackgroundColor()" class="d-flex"
            ><v-toolbar-title :style="getEventTextColor()">
              <v-text-field
                class="mt-4"
                placeholder="Event Name"
                :style="{
                  color: getEventTextColor(),
                }"
                v-model:model-value="title"
              ></v-text-field></v-toolbar-title
          ></v-toolbar>
          <v-form class="pt-4">
            <v-select
              :items="getSourceNames()"
              class="px-4"
              v-model:model-value="eventType"
              :rules="[(v) => !!v || 'Event type must be selected']"
              dense
              label="Event Type"
            ></v-select>
            <v-select
              :items="getSquadronDesignations()"
              class="px-4"
              v-model:model-value="requiredSquadrons"
              dense
              multiple
              label="Required Squadrons"
            ></v-select>
            <v-textarea
              class="text-body-2 px-4"
              v-model:model-value="description"
              placeholder="Markdown Supported Text Area"
              label="Event Description"
            ></v-textarea>
          </v-form>
        </div>
        <div id="menu-page-edit" v-if="menuPage === 'timespan'">
          <v-toolbar :color="getEventBackgroundColor()" class="d-flex"
            ><v-toolbar-title
              :style="{
                color: getEventTextColor(),
              }"
              >{{ title }}</v-toolbar-title
            ></v-toolbar
          >

          <v-form class="pt-4">
            <v-row class="pb-4">
              <v-col cols="6">
                <h3 class="px-4">Event Start</h3>
                <Datepicker
                  class="px-4"
                  v-model="start"
                  minutesIncrement="30"
                  minutesGridIncrement="30"
                  :is24="false"
                  inline
                  textInput
                  inlineWithInput
                  autoApply
                  :flow="['calendar', 'time']"
                  :clearable="false"
                ></Datepicker>
              </v-col>
              <v-col cols="6">
                <h3 class="px-4">Event End</h3>
                <Datepicker
                  class="px-4"
                  v-model="end"
                  minutesIncrement="30"
                  minutesGridIncrement="30"
                  :is24="false"
                  :flow="['calendar', 'time']"
                  inline
                  textInput
                  inlineWithInput
                  autoApply
                  :clearable="false"
                ></Datepicker>
              </v-col>
            </v-row>
          </v-form>
        </div>
        <div id="menu-page-recurring" v-if="menuPage === 'recurring'">
          <v-toolbar :color="getEventBackgroundColor()" class="d-flex"
            ><v-toolbar-title
              :style="{
                color: getEventTextColor(),
              }"
              >{{ title }}</v-toolbar-title
            >
          </v-toolbar>
          <v-form class="py-4">
            <v-select
              :items="['Never', 'Weekly', 'Bi-Weekly', 'Monthly']"
              class="px-4"
              v-model:model-value="recurring"
              dense
              label="Event Recurrence"
            ></v-select>
            <div class="px-4">
              <div class="text-caption">Number of Recurrences</div>
              <v-slider
                min="0"
                max="12"
                step="1"
                show-ticks
                thumb-label
                :disabled="recurring === 'Never'"
                v-model:model-value="recurrences"
                label="Recurrence Stop Date"
              ></v-slider>
            </div>
          </v-form>
          <div class="text-caption px-4">Recurring Dates</div>
          <v-row class="px-4">
            <v-col
              xs="12"
              md="4"
              cols="3"
              v-for="date in computeRecurrences.slice(1)"
            >
              <v-card :color="getEventBackgroundColor()">
                <v-card-title :style="{ color: getEventTextColor() }">{{
                  date.toDateString()
                }}</v-card-title>
              </v-card>
            </v-col>
          </v-row>
        </div>
      </v-main>
    </v-layout>
  </v-card>
</template>

<script>
import MarkdownComponent from "./MarkdownComponent.vue";
import Datepicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import { mapGetters } from "vuex";
import { eventSources } from "../assets/js/eventSources";
import axios from "axios";
import { RRule } from "rrule";
import { DateTime } from "luxon";

export default {
  name: "EventComponent",
  components: { MarkdownComponent, Datepicker },
  props: ["event"],
  emits: ["dialogClose"],
  data: function () {
    return {
      drawer: true,
      description: this.event.extendedProps.description,
      menuPage: "display",
      title: this.event.title,
      requiredSquadrons: this.event.extendedProps.required_squadrons
        ? this.event.extendedProps.required_squadrons.map((x) => x.designation)
        : [],
      eventType: this.event.source
        ? this.event.source.internalEventSource.meta.extraParams.type
        : null,
      recurring: "Never",
      start: this.event.start,
      end: this.event.end,
      recurrences: 0,
    };
  },
  computed: {
    ...mapGetters(["squadrons"]),
    computeRecurrences: function () {
      const rule = new RRule({
        freq: this.recurring === "Monthly" ? RRule.MONTHLY : RRule.WEEKLY,
        interval: this.recurring === "Bi-Weekly" ? 2 : 1,
        dtstart: this.event.start,
        count: this.recurrences + 1,
      });

      return rule.all();
    },
  },

  methods: {
    getEventSource: function () {
      return eventSources.find(
        (element) => element.extraParams.type === this.eventType
      );
    },
    getEventBackgroundColor: function () {
      let eventSource = this.getEventSource();

      if (eventSource) {
        return eventSource.backgroundColor;
      } else {
        return "#F6AE2D";
      }
    },
    getEventTextColor: function () {
      let eventSource = this.getEventSource();

      if (eventSource) {
        return eventSource.textColor;
      } else {
        return "black";
      }
    },
    commitEvent: async function () {
      const common_event_properties = {
        name: this.title,
        description: this.description,
        type: this.eventType,
        required_squadrons: this.squadrons
          .filter((x) => this.requiredSquadrons.includes(x.designation))
          .map((x) => x.id),
      };

      if (this.end < this.start) {
        let end = new Date(this.start);

        end.setMinutes(end.getMinutes() + 30);

        this.end = end;
      }

      if (this.event.id) {
        const updated_event = {
          id: this.event.id,
          start: this.start.toISOString(),
          end: this.end.toISOString(),
          ...common_event_properties,
        };

        await this.updateSchedule(updated_event.id, updated_event);
      } else {
        const start = DateTime.fromJSDate(this.start);
        const end = DateTime.fromJSDate(this.end);
        const timeDelta = end.diff(start);

        for (const occurrence of this.computeRecurrences) {
          const occurrenceStart = DateTime.fromJSDate(occurrence);
          const occurrenceEnd = occurrenceStart.plus(timeDelta);

          const new_event = {
            start: occurrenceStart.toISO(),
            end: occurrenceEnd.toISO(),
            ...common_event_properties,
          };
          await this.addToSchedule(new_event);
        }
      }

      this.event.remove();
      this.$emit("dialogClose");
    },
    removeEvent: async function () {
      if (this.event.id) {
        await this.removeFromSchedule(this.event.id);
      }

      this.event.remove();
      this.$emit("dialogClose");
    },
    getSourceNames: function () {
      return eventSources.map((x) => x.extraParams.type);
    },
    gotoMenuPage(page) {
      if (page === this.menuPage) {
        this.menuPage = "display";
      } else {
        this.menuPage = page;
      }
    },
    getSquadronDesignations: function () {
      return this.squadrons.map((x) => x.designation);
    },
    addToSchedule: async function (event) {
      await axios.post("/api/roster/event/list/", event);
    },
    updateSchedule: async function (id, event) {
      const response = await axios.put(
        `/api/roster/event/detail/${id}/`,
        event
      );
    },
    removeFromSchedule: async function (id) {
      const response = await axios.delete(`/api/roster/event/detail/${id}/`);
    },
  },
};
</script>

<style scoped>
.display-window {
  width: 50vw;
  height: 70vh;
}

.fixedBottom {
  position: fixed;
  bottom: 0;
  width: 100%;
}
</style>

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
        </v-list>
        <v-spacer></v-spacer>
        <v-list nav>
          <v-list-item
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
          <v-spacer></v-spacer>
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
          <v-form class="py-4">
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
import { mapGetters } from "vuex";
import { eventSources } from "../assets/js/eventSources";
import axios from "axios";
import { RRule } from "rrule";

export default {
  name: "EventComponent",
  components: { MarkdownComponent },
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
      recurrences: 0,
    };
  },
  computed: {
    ...mapGetters(["squadrons"]),
    computeRecurrences: function () {
      const ruleMap = {
        Weekly: RRule.WEEKLY,
        "Bi-Weekly": RRule.WEEKLY,
        Monthly: RRule.MONTHLY,
        Never: null,
      };

      const intervalMap = {
        Weekly: 1,
        "Bi-Weekly": 2,
        Monthly: 1,
        Never: 0,
      };

      if (this.recurring !== "Never" && this.recurrences) {
        const rule = new RRule({
          freq: ruleMap[this.recurring],
          interval: intervalMap[this.recurring],
          dtstart: this.event.start,
          count: this.recurrences + 1,
        });
        return rule.all();
      } else {
        return [];
      }
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
      let new_event = {
        start: this.event.startStr,
        end: this.event.endStr,
        name: this.title,
        description: this.description,
        type: this.eventType,
        required_squadrons: this.squadrons
          .filter((x) => this.requiredSquadrons.includes(x.designation))
          .map((x) => x.id),
      };

      if (this.event.id) {
        new_event.id = this.event.id;
        await this.updateSchedule(this.event.id, new_event);
        this.event.remove();
      } else {
        await this.addToSchedule(new_event);
        this.event.remove();
      }

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
  position: fixed !important;
  bottom: 0 !important;
  width: 100%;
}
</style>

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
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-content-save"
            title="Save"
            value="save"
            @click="commitEvent"
          ></v-list-item>
          <v-spacer></v-spacer>
          <v-list-item
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
          <v-toolbar
            :color="
              event.source
                ? event.source.internalEventSource.ui.backgroundColor
                : '#F6AE2D'
            "
            class="d-flex"
            ><v-toolbar-title
              :style="{
                color: event.source
                  ? event.source.internalEventSource.ui.textColor
                  : 'black',
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
          <v-toolbar
            :color="
              event.source
                ? event.source.internalEventSource.ui.backgroundColor
                : '#F6AE2D'
            "
            class="d-flex"
            ><v-toolbar-title
              :style="{
                color: event.source
                  ? event.source.internalEventSource.ui.textColor
                  : 'black',
              }"
            >
              <v-text-field
                class="mt-4"
                placeholder="Event Name"
                :style="{
                  color: event.source
                    ? event.source.internalEventSource.ui.textColor
                    : 'black',
                }"
                v-model:model-value="title"
              ></v-text-field></v-toolbar-title
          ></v-toolbar>
          <v-select
            :items="getSourceNames()"
            class="px-4"
            v-model:model-value="eventType"
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
          ></v-textarea>
        </div>
      </v-main>
    </v-layout>
  </v-card>
</template>

<script>
import MarkdownComponent from "./MarkdownComponent.vue";
import { mapGetters } from "vuex";

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
    };
  },
  computed: {
    ...mapGetters(["squadrons"]),
  },

  methods: {
    commitEvent: function () {
      this.event.setProp("title", this.title);
      this.event.setExtendedProp("description", this.description);
      this.$emit("dialogClose");
      // this.getCalendar().refetchEvents() todo enable for pulling updated data
    },
    removeEvent: function () {
      this.event.remove();
      this.$emit("dialogClose");
      // this.getCalendar().refetchEvents() todo enable for pulling updated data
    },
    getCalendar: function () {
      return this.event._context.calendarApi;
    },
    getSources: function () {
      return this.getCalendar().getEventSources();
    },
    getSourceNames: function () {
      return this.getSources().map(
        (x) => x.internalEventSource.meta.extraParams.type
      );
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
  },
};
</script>

<style scoped>

.display-window {
  min-width: 50vw;
  max-width: 70vw;
  min-height: 50vh;
  max-height: 70vh;
}

</style>

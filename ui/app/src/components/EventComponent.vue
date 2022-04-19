<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer expand-on-hover rail>
        <v-list nav>
          <v-list-item
            :prepend-icon="!editDescription ? 'mdi-xml' : 'mdi-text-box'"
            :title="!editDescription ? 'Edit' : 'View'"
            value="description"
            @click="editDescription = !editDescription"
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

      <v-main style="min-height: 50vh; min-width: 50vh">
        <div id="event-display-static" v-if="!editDescription">
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
            v-if="!editDescription"
            :content="description"
            class="pa-4"
          ></MarkdownComponent>
        </div>
        <div id="event-display-edit" v-if="editDescription">
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
          <v-textarea
            v-model:model-value="description"
            max-rows="10"
            class="pa-4"
            placeholder="Markdown Supported Text Area"
          ></v-textarea>
        </div>
      </v-main>
    </v-layout>
  </v-card>
</template>

<script>
import MarkdownComponent from "./MarkdownComponent.vue";

export default {
  name: "EventComponent",
  components: { MarkdownComponent },
  props: ["event"],
  emits: ["dialogClose"],
  data: function () {
    return {
      drawer: true,
      description: this.event.extendedProps.description,
      editDescription: false,
      title: this.event.title,
    };
  },
  methods: {
    commitEvent: function () {
      this.event.setProp("title", this.title);
      this.event.setExtendedProp("description", this.description);
    },
    removeEvent: function () {
      this.event.remove();
      this.$emit("dialogClose");
    },
  },
};
</script>

<style scoped></style>

<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer expand-on-hover rail class="d-flex fill-height">
        <v-list density="compact" nav>
          <v-list-item
            :prepend-icon="!editDescription ? 'mdi-xml' : 'mdi-code-tags'"
            title="Description"
            value="myfiles"
            @click="editDescription = !editDescription"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-account-multiple"
            title="Shared with me"
            value="shared"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-star"
            title="Starred"
            value="starred"
            @click="commitEvent"
          ></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-main style="min-height: 50vh; min-width: 50vh">
        <v-toolbar :color="event.source ? event.source.internalEventSource.ui.backgroundColor : '#F6AE2D'"
          ><span :style="{color: event.source ? event.source.internalEventSource.ui.textColor : 'black'}">{{ event.title }}</span>
        </v-toolbar>
        <MarkdownComponent
          v-if="!editDescription"
          :content="description"
        ></MarkdownComponent>
        <v-textarea v-if="editDescription" v-model:model-value="description" auto-grow ></v-textarea>
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
      description: "# hello",
      editDescription: false,
    };
  },
  methods: {
    commitEvent: function () {
      console.log(this.event);
    },
  },
};
</script>

<style scoped></style>

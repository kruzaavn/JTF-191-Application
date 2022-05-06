function formatEvent(eventData) {
  return { title: eventData.name, ...eventData };
}

const eventDefaults = {
  url: "/api/roster/event/list/",
  eventDataTransform: formatEvent,
  editable: true,
};

export const eventSources = [
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
];

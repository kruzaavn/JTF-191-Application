import axios from "axios";

const state = {
  rosterList: [],
  squadronList: [],
  hqs: [],
  dcsModules: [],
  documentationList: [],
  documentationModuleList: [],
  photos: [],
  storesList: [],
  munitionList: [],
  operationList: [],
  aviator: { callsign: "" },
  leavesOfAbsence: [],
};

const mutations = {
  setRoster(state, roster) {
    state.rosterList = roster;
  },
  setSquadrons(state, squadrons) {
    state.squadronList = squadrons;
  },
  setHQs(state, HQs) {
    state.hqs = HQs;
  },
  setDcsModules(state, modules) {
    state.dcsModules = modules;
  },
  addEvent(state, event) {
    state.schedule.push(event);
  },
  removeEvent(state, event) {
    const index = state.schedule.findIndex(
      (element) => element.id === event.id
    );
    state.schedule.splice(index, 1);
  },
  updateEvent(state, event) {
    const index = state.schedule.findIndex(
      (element) => element.id === event.id
    );
    state.schedule.splice(index, 1, event);
  },
  setDocumentation(state, documentation) {
    state.documentationList = documentation;
  },
  setDocumentationModules(state, modules) {
    state.documentationModuleList = modules;
  },
  setPhotos(state, photos) {
    state.photos = photos;
  },
  setMunition(state, munitions) {
    state.munitionList = munitions;
  },
  setStores(state, stores) {
    state.storesList = stores;
  },
  setOperations(state, operations) {
    state.operationList = operations;
  },
  setAviator(state, aviator) {
    state.aviator = aviator;
  },
};

const getters = {
  roster: (state) => state.rosterList,
  squadrons: (state) => state.squadronList,
  hqs: (state) => state.hqs,
  aviator: (state) => state.aviator,
  dcsModules: (state) => state.dcsModules,
  documentation: (state) => state.documentationList,
  documentationModules: (state) => state.documentationModuleList,
  photos: (state) => state.photos,
  munitions: (state) => state.munitionList,
  stores: (state) => state.storesList,
  leavesOfAbsence: (state) => state.leavesOfAbsence,
  munitionsTable: (state) => {
    let table = state.storesList.reduce((acc, element) => {
      const previous = acc.find(
        (x) =>
          x.munition === element.munition && x.squadron === element.squadron
      );

      if (previous) {
        previous.count += element.count;
      } else {
        const munition = state.munitionList.find(
          (x) => x.id === element.munition
        );
        element.munition_name = munition.name;
        element.munition_type = munition.munition_type
          .replaceAll("_", " ")
          .toUpperCase();
        element.squadron_name = state.squadronList.find(
          (x) => x.id === element.squadron
        ).name;
        acc.push(element);
      }
      return acc;
    }, []);

    return table;
  },
  operations: (state) => {
    return state.operationList;
  },
};

const actions = {
  async getRoster({ commit }) {
    const response = await axios.get("/api/roster/aviators/list/");
    commit("setRoster", response.data);
  },
  async getSquadrons({ commit }) {
    const response = await axios.get("/api/roster/squadrons/list/");
    commit("setSquadrons", response.data);
  },
  async getHQs({ commit }) {
    const response = await axios.get("/api/roster/hqs/list/");
    commit("setHQs", response.data);
  },
  async getDcsModules({ commit }) {
    const response = await axios.get("/api/roster/modules/list/");
    commit("setDcsModules", response.data);
  },
  async getDocumentation({ commit }) {
    const response = await axios.get("/api/roster/documentation/list/");
    commit("setDocumentation", response.data);
  },
  async getDocumentationModules({ commit }) {
    const response = await axios.get("/api/roster/documentation/modules/list/");
    commit("setDocumentationModules", response.data);
  },
  async getPhotos({ commit }) {
    const response = await axios.get("/api/roster/user_images/list/");
    commit("setPhotos", response.data);
  },
  async getMunitionsList({ commit }) {
    const response = await axios.get("/api/roster/munition/list/");
    commit("setMunition", response.data);
  },
  async getStoresList({ commit }, operationName) {
    const response = await axios.get(
      `/api/roster/stores/list/${operationName}/`
    );
    commit("setStores", response.data);
  },
  async getOperations({ commit }) {
    const response = await axios.get("/api/roster/operation/list");
    commit("setOperations", response.data);
  },
  async getAviatorFromUser({ commit }, userId) {
    const token = localStorage.getItem("token");
    const config = {
      headers: { Authorization: `Bearer ${token}` },
    };
    const response = await axios.get(
      `/api/roster/aviators/fromuser/${userId}/`,
      {},
      config
    );
    commit("setAviator", response.data);
  },
  async getAviator({ commit }, aviatorId) {
    const response = await axios.get(
      `/api/roster/aviators/detail/${aviatorId}/`
    );
    commit("setAviator", response.data);
  },
};

export default {
  state,
  mutations,
  getters,
  actions,
};

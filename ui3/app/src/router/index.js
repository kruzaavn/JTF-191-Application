import { createRouter, createWebHashHistory } from "vue-router";
import AboutView from "@/views/AboutView";
import GCI from "@/views/GCI.vue";
import QualificationView from "@/views/QualificationView";
import SquadronView from "@/views/SquadronView";
import JoinUs from "@/views/JoinUs";
import ScheduleView from "@/views/ScheduleView";
import RegisterView from "@/views/RegisterView";
import SquadronList from "@/views/SquadronList";
import PhotosView from "@/views/PhotosView";
import OperationView from "@/views/OperationView";
import OperationList from "@/views/OperationList";
import ProfileView from "@/views/ProfileView";

const title_header = "JTF-191";

function title(header, title) {
  return `${header} - ${title}`;
}

const routes = [
  {
    path: "/",
    name: "Home",
    component: PhotosView,
    meta: {
      title: title(title_header, "Photos"),
    },
  },
  {
    path: "/about",
    name: "About",
    component: AboutView,
    meta: {
      title: title(title_header, "About Us"),
    },
  },
  {
    path: "/profile",
    name: "Profile",
    component: ProfileView,
    meta: {
      title: title(title_header, "Aviator Profile"),
    },
  },
  {
    path: "/server",
    name: "GCI",
    component: GCI,
    meta: {
      title: title(title_header, "Servers"),
    },
  },
  {
    path: "/squadron/:squadronDesignation",
    name: "Squadron",
    component: SquadronView,
    props: true,
    meta: {
      title: title(title_header, "Squadrons"),
    },
  },
  {
    path: "/squadron",
    name: "SquadronList",
    component: SquadronList,
    meta: {
      title: title(title_header, "Squadrons"),
    },
  },
  {
    path: "/joinus",
    name: "JoinUs",
    component: JoinUs,
    meta: {
      title: title(title_header, "Join Us"),
    },
  },
  {
    path: "/schedule",
    name: "Schedule",
    component: ScheduleView,
    meta: {
      title: title(title_header, "Schedule"),
    },
  },
  {
    path: "/qualification/:qualificationModule",
    name: "Qualification",
    props: true,
    component: QualificationView,
    meta: {
      title: title(title_header, "Qualifications"),
    },
  },
  {
    path: "/register/:id",
    name: "Register",
    props: true,
    component: RegisterView,
    meta: {
      title: title(title_header, "Register"),
    },
  },
  {
    path: "/operation",
    name: "OperationList",
    component: OperationList,
    meta: {
      title: title(title_header, "Operations"),
    },
  },
  {
    path: "/operation/:operationName",
    name: "Operation",
    component: OperationView,
    props: true,
    meta: {
      title: title(title_header, "Operations"),
    },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;

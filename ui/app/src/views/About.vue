<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>ABOUT US</h1>
        <p>
          JTF-191 was formed in June of 2020 and is composed of
          {{ squadrons.length }} squadrons with {{ roster.length }} active
          members. We operate as a milsim group with an emphasis on realism and
          joint operations with all branches of military aviation. We have a
          detailed training program for all new pilots that focuses on teaching
          a working knowledge of the airframe and relevant tactics. Our training
          is built to both teach new pilots about their chosen airframes or to
          provide refreshers to experienced pilots. With detailed courses on
          everything from take-off and landings to air-to-air tactics, the
          training program is designed to ensure you are comfortable in your
          role and up to the task of joining our ranks. Upon finishing your
          training you are placed into an operational squadron with custom
          liveries made just for you. Each squadron handles their own training,
          keeping their pilots skills up to par with the unit standards. We have
          two dedicated servers that are up 24/7 and a unit-wide mission night
          every Saturday. Saturday missions range from fun PvP missions to
          organized pre-planned sorties built in an ongoing deployment campaign.
        </p>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <h1>TF-191 Guiding Values</h1>
        <ol>
          <li>
            We are here to have fun. As much as we seek enjoyment in
            role-playing a military organization we must take stock in the fact
            that this is a video game. It is acceptable for priorities such as
            work, family, and your wider community to take precedence over what
            we do here. It is also acceptable to take a step back from time to
            time and ask yourself if you are enjoying yourself with us and, if
            not, seek measures to change that.
          </li>
          <li>
            Rank has its place but it shouldn’t be confused with leadership. One
            of the interesting things about our organization is that we have a
            hierarchy of rank. This serves many different purposes but chief
            among them is to recognize individuals for their accomplishments and
            contributions. However, we must never forget that these are titles
            that we impose on ourselves and are meaningless outside of our group
            and more importantly doesn't mean that leadership can’t come from
            below. We must strive to recognize leadership when it is apparent.
          </li>
          <li>
            We are a community of like-minded pilots and we are stronger when we
            pursue a common goal. With as many pilots as we have, we will
            struggle at times for a common vision and definition. We must strive
            to understand others' differences in opinion and reconcile them.
            This may not happen fast or satisfactorily resolve in favor of your
            viewpoint but each of us owes it to each other to participate in the
            discussion and accept the outcomes.
          </li>
          <li>
            Attention to realism. We want to, as much as practicable, replicate
            real-world military units and their operations. We should be
            cognizant that many people can have a rudimentary understanding of
            the military and some of the information that is out there is
            untrustworthy. We have many members who are veterans with first-hand
            experience at different levels who can inform us with their
            experience, however, the military is a large organization with many
            different parts and very few of us experience it all.
          </li>
          <li>
            All members must act with integrity. It is unfortunate but the
            reality is that we will not always get our way. It is important
            though that while recognizing this fact, we always treat each other
            fairly and above reproach.
          </li>
        </ol>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <h1>
          If JTF-191 interests you please go to our
          <router-link to="/joinus">Recruitment Page</router-link>
        </h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-carousel cycle>
          <v-carousel-item
            v-for="(image, index) in squadronImages"
            :key="index"
            reverse-transition="fade-transition"
            transition="fade-transition"
          >
            <v-img contain :src="image" :height="250"> </v-img>
          </v-carousel-item>
        </v-carousel>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'About',
  computed: {
    ...mapGetters(['roster', 'squadrons']),
    squadronImages: function () {
      return this.squadrons.map((x) => x.img)
    },
  },
}
</script>

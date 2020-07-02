<template>
    <v-container>
        <v-col>
            <v-row>
            <h1>ABOUT US</h1>
            <p>JTF-191 was formed in June of 2020 and is composed of ([squadron.length)] squadrons with ([roster.length]) active members.
                We operate as a milsim group with an emphasis on realism and joint operations with all branches of military aviation.
                We have a detailed training program for all new pilots that focuses on teaching a working knowledge of the airframe and relevant tactics.
                Our training is built to both teach new pilots about their chosen airframes or to provide refreshers to experienced pilots.
                With detailed courses on everything from take-off and landings to air-to-air tactics, the training program is designed to ensure you are
                comfortable in your role and up to the task of joining our ranks.
                Upon finishing your training you are placed into an operational squadron with custom liveries made just for you.
                Each squadron handles their own training, keeping their pilots skills up to par with the unit standards.
                We have two dedicated servers that are up 24/7 and a unit-wide mission night every Saturday.
                Saturday missions range from fun PvP missions to organized pre-planned sorties built in an ongoing deployment campaign.</p>
            <br>
            <br>
            </v-row>
            <v-row>
            <h1>Below are the guiding values for TF-191.</h1>

            <template>
                <v-list-item>
                    <v-list-item-content>
                        <v-list-item-title>We are here to have fun. As much as we seek enjoyment in role-playing a
                            military organization we must take stock in the fact that this is a video game. It is acceptable for
                            priorities such as work, family, and your wider community to take precedence over what we do here.
                            It is also acceptable to take a step back from time to time and ask yourself if you are enjoying yourself with us and,
                            if not, seek measures to change that.
                        </v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-content>
                        <v-list-item-title>Rank has its place but it shouldn’t be confused with leadership.
                            One of the interesting things about our organization is that we have a hierarchy of rank.
                            This serves many different purposes but chief among them is to recognize individuals for
                            their accomplishments and contributions. However, we must never forget that these are titles that we
                            impose on ourselves and are meaningless outside of our group and more importantly doesn't mean that
                            leadership can’t come from below. We must strive to recognize leadership when it is apparent.
                        </v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item>

                    <v-list-item-content>
                        <v-list-item-title>We are a community of like-minded pilots and we are stronger when we pursue a common goal.
                            With as many pilots as we have, we will struggle at times for a common vision and definition.
                            We must strive to understand others' differences in opinion and reconcile them.
                            This may not happen fast or satisfactorily resolve in favor of your viewpoint but each of us owes
                            it to each other to participate in the discussion and accept the outcomes.
                        </v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-content>
                        <v-list-item-title>Attention to realism. We want to, as much as practicable,
                            replicate real-world military units and their operations. We should be cognizant that many people
                            can have a rudimentary understanding of the military and some of the information that is out there is untrustworthy.
                            We have many members who are veterans with first-hand experience at different levels who can inform us with their experience,
                            however, the military is a large organization with many different parts and very few of us experience it all.
                        </v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-content>
                        <v-list-item-title>All members must act with integrity. It is unfortunate but the reality is that we will not always get our way.
                            It is important though that while recognizing this fact, we always treat each other fairly and above reproach.
                        </v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </template>


            <h2> If JTF-171 interests you please go to our recruitment page</h2>

            <template>
                <v-card
                        class="mx-auto"
                        max-width="344"
                        outlined
                >
                    <v-list-item one-line>
                        <v-list-item-content>
                            <div class="overline mb-4">OVERLINE</div>
                            <v-list-item-title class="headline mb-1">Recruitment Page</v-list-item-title>
                        </v-list-item-content>

                        <v-list-item-avatar
                                tile
                                size="80"
                                color="grey"
                        ></v-list-item-avatar>
                    </v-list-item>

                    <v-card-actions>
                        <v-btn
                                Join
                                Us to='<LINKHERE>'></v-btn>
                    </v-card-actions>
                </v-card>

            </template>
        </v-row>
        </v-col>

    </v-container>
</template>
<template>
  <v-carousel>
    <v-carousel-item
      squadron_images function() {
      return this.squadrons.map(x => x.img)
        }
      reverse-transition="fade-transition"
      transition="fade-transition"
    ></v-carousel-item>
  </v-carousel>
</template>
<script>
import {mapGetters} from 'vuex'
export default {
        name: 'About',
        computed: {
        ...mapGetters (['roster'],(['squadrons']))
        }
    }
 </script>

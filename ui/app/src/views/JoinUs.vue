<template>
    <v-container>
        <h1>Join Us</h1>
        <p>Requirements to join JTF-191</p>
        <ul>
            <li>18 years or older</li>
            <li>Cockpit visualization, VR headset or Track IR</li>
            <li>Hands on throttle and stick (HOTAS)</li>
            <li>Be able to attend a training and mission night each week or let us know that you can not make it</li>
            <li>Have a good attitude and a willingness to learn</li>
        </ul>
        <v-form>
            <v-row>
                <v-col>
                    <v-row>
                        <v-checkbox
                                v-model="age"
                                :rules="[v => !!v || 'You must be over the age of 18!']"
                                label="Are you over 18?"
                        ></v-checkbox>
                    </v-row>
                    <v-row>
                        <v-checkbox
                                v-model="valueStatement"
                                :rules="[v => !!v || 'You must read out statement of values']"
                                label="Have you read our Statement of Values?"
                        ></v-checkbox>
                    </v-row>
                    <v-row>
<!--                        Doing a timezone drop down menu is a huge headache-->
                        <v-checkbox
                                v-model="attendance"
                                :rules="[v => !!v || 'You must be able to attend content at 2000 EST!']"
                                label="Are you able to attend mission nights at 2000 EST?"
                        ></v-checkbox>
                    </v-row>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-text-field
                            v-model="joinUsForm.first_name"
                            label="First Name"
                            required
                    >
                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            v-model="joinUsForm.last_name"
                            label="Last Name"
                            required
                    >
                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            v-model="joinUsForm.email"
                            type="email"
                            label="E-mail"
                            required
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-text-field
                            v-model="joinUsForm.callsign"
                            label="Callsign"
                            required
                    >
                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            v-model="joinUsForm.hotas"
                            label="Type of HOTAS"
                            required
                    >
                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            v-model="joinUsForm.head_tracking"
                            label="Type of Head tracking or VR"
                            required
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-text-field
                            v-model="joinUsForm.discord"
                                label="Discord Name"
                                required
                        >
                    </v-text-field>
                </v-col>
            </v-row>
            <v-row align="center">
                <v-col cols="12" sm="6">
                    <v-select
                            v-model="joinUsForm.dcs_modules"
                            :items="dcsModules.filter(x => x.module_type === 'aircraft').map(x => x.name)"
                            :menu-props="{ maxHeight: '400' }"
                            label="Airframes"
                            multiple
                            hint="Pick your owned modules"
                            persistent-hint
                    ></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                    <v-select
                            v-model="joinUsForm.dcs_modules"
                            :items="dcsModules.filter(x => x.module_type === 'map').map(x => x.name)"
                            :menu-props="{ maxHeight: '400' }"
                            label="Maps"
                            multiple
                            hint="Pick your owned modules"
                            persistent-hint
                    ></v-select>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12">
                    <v-textarea
                            v-model="joinUsForm.about"
                            auto-grow
                            clearable
                            label="Tell Us about yourself"
                            hint="Briefly describe what you are looking for and how we are a good fit for you?"
                            rows="1"
                    >
                    </v-textarea>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <div class="my-2">
                        <v-btn outlined tile color="Submit">Submit</v-btn>
                    </div>
                </v-col>
            </v-row>
        </v-form>
    </v-container>
</template>


<script>
    import {mapGetters, mapActions} from 'vuex'
    export default {
        name: 'JoinUs',
        computed: {
            ...mapGetters(['dcsModules'])
        },
        methods: {
            ...mapActions(['getDcsModules'])
        },
        mounted() {
            this.getDcsModules()
        },
        data: () => ({
            joinUsForm: {
                // form data for api submission, changed variable style to
                // api format.
                first_name: '',
                last_name: '',
                email: '',
                callsign: '',
                hotas: '',
                head_tracking: '',
                dcs_modules: [],
                about: '',
                discord: ''
            },
            attendance: false,
            age: false,
            valueStatement: false,
        })
    }
</script>

<style>


</style>
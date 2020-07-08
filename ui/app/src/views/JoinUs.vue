<template>

    <v-container>
        <h1>Join Us</h1>
        <p>Requirements to join the unit</p>
        <ul>
            <li>Have headtracking or VR</li>
            <li>A HOTAS</li>
            <li>Be able to attend a training and mission night each week or let us know that you can not make it</li>
            <li>Have a good attitude and a willingness to learn</li>
            <li>Be 18 years or older</li>
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
                            v-model="firstName"

                            label="First Name"
                            required
                    >

                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            v-model="lastName"

                            label="Last Name"
                            required
                    >

                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            v-model="email"
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
                            v-model="callSign"
                            label="Callsign"
                            required
                    >

                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            v-model="hotas"

                            label="Type of HOTAS"
                            required
                    >

                    </v-text-field>
                </v-col>

                <v-col>
                    <v-text-field
                            v-model="headTracking"

                            label="Type of Headtracking or VR"
                            required
                    >

                    </v-text-field>
                </v-col>

            </v-row>

            <v-row>
                <v-col>
                    <v-text-field
                            v-model="discord"

                            label="Discord Name"
                            required
                    >

                    </v-text-field>
                </v-col>
            </v-row>

            <v-row align="center">
                <v-col cols="12" sm="6">
                    <v-select
                            v-model="ownedModules"
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
                            v-model="ownedModules"
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
                <v-col>
                    <div class="my-2">
                        <v-btn small color="Submit">Submit</v-btn>
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
            firstName: '',
            lastName: '',
            email: '',
            attendance: false,
            callSign: '',
            hotas: '',
            headTracking: '',
            ownedModules: [],
            age: false,
            valueStatement: false,

        })

    }

</script>

<style>


</style>
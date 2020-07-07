<template>

    <v-container>
        <h1>Join Us</h1>
        <p>Requirements to join the unit</p>
        <ul>
            <li>Have headtracking or VR</li>
            <li>A Hotas</li>
            <li>Be able to attend a training and mission night each week or let us know that you can not make it</li>
            <li>Have a good attitude and a willingness to learn</li>
            <li>Be 18 years or older</li>
        </ul>


        <v-form>
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
<!--drop down menu                    -->
                    <v-text-field
                            v-model="timeZone"
                            label="Time Zone"
                            required
                    >

                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            v-model="hotas"

                            label="Type of Hotas"
                            required
                    >

                    </v-text-field>
                </v-col>
                <v-row>
                    <v-col>
                        <v-text-field
                                v-model="headTracking"

                                label="Type of Headtracking or VR"
                                required
                        >

                        </v-text-field>
                    </v-col>

                </v-row>
            </v-row>
            <v-row align="center">
                <v-col cols="12" sm="6">
                    <v-subheader v-text="'Airframes'"></v-subheader>
                </v-col>
                <v-col cols="12" sm="6">
                    <v-select
                            v-model="ownedModules"
                            :items="dcsModules"
                            :menu-props="{ maxHeight: '400' }"
                            label="Select"
                            multiple
                            hint="Pick your owned modules"
                            persistent-hint
                    ></v-select>
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
        mounted () {
            this.getDcsModules()
        },
        data:() => ({
            firstName: '',
            lastName: '',
            email: '',
            timeZone: '',
            callSign: '',
            hotas: '',
            headTracking: '',
            ownedModules: [],

        })

    }

</script>

<style>


</style>
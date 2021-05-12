<template>
    <v-container fluid>
        <v-row align-content= 'start'>
            <v-col>
                <v-card-title>
                    Operation: {{operation.name}}
                    Start Date: {{operation.start}}
                </v-card-title>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-card-title>
                    Theater Stores
                </v-card-title>
                <v-card-text>
                    <v-row>
                        <v-col>
                            <h4>
                                Overall Stores
                            </h4>
                            <v-data-table
                                dense
                                :headers="munitionsHeaders"
                                :items="toMunitionsTable(munitions.stats.count)"
                            >
                            </v-data-table>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-col>
        </v-row>
    </v-container>
        
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    name: 'Munitions',
    data: () => ({

    munitionsHeader: [
        {
            text: 'Munition',
            align: 'start',
            sortable: true,
            value: 'munition',
        },
        {
            text: 'Count',
            sortable: true,
            align: 'start',
            value: 'count',

        },
    }),
    
    computed: {
        ...mapGetters(['munitions']),
        members: function (){
            return this.roster.filter 

                        
        }
        

    }
}
</script> 
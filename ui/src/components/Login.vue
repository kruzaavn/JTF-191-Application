<template>

 <div class="text-center">
    <v-dialog
      v-model="dialog"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="white"
          outlined
          v-bind="attrs"
          v-on="on"
        >
          <v-icon left>mdi-login</v-icon>Login
        </v-btn>
      </template>

      <v-card>
        <v-card-title
          primary-title
        >
          <h1>Login</h1>
        </v-card-title>
        <v-card-text>
        <v-form>
          <v-text-field label="username"></v-text-field>
          <v-text-field label="password" type="password"></v-text-field>
        </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn outlined>Register</v-btn>
          <v-spacer></v-spacer>
          <v-btn outlined>Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>


</template>

<script>
    export default {
        name: "Login",
        data() {
          return {
            dialog: false
          }
        }
    }
</script>

<style scoped>

</style>
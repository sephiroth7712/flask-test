<template>
  <div id="app">
    <head>
      <link
        href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons"
        rel="stylesheet"
      />
    </head>
    <v-app id="inspire">
      <div>
        <v-toolbar color="#2490ef">
          <router-link :to="{ path: '/' }"
            ><v-toolbar-title class="white--text"
              >Inventory Management System</v-toolbar-title
            ></router-link
          >

          <v-spacer></v-spacer>

          <v-toolbar-items>
            <v-btn class="white--text" to="/products" text>Products</v-btn>
            <v-btn class="white--text" to="/locations" text>Locations</v-btn>
            <v-btn class="white--text" to="/movements" text
              >Product Movements</v-btn
            >
          </v-toolbar-items>
        </v-toolbar>
        <router-view />
      </div>
    </v-app>
  </div>
</template>

<script>
export default {
  name: "App",

  data: () => ({
    //
  }),
};
</script>
<style>
a {
  text-decoration: none;
}
</style>

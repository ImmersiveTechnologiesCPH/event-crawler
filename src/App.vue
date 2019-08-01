<template>
  <v-app>
    <v-toolbar dense app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Absolute Zero</span>
        <span class="font-weight-light"> Event Crawler</span>
      </v-toolbar-title>
    </v-toolbar>
    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      //
    }
  }
}
</script>

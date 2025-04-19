<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Brewery Explorer</v-toolbar-title>
    </v-app-bar>
    <v-main>
      <BreweryTable />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
  import BreweryTable from '@/components/BreweryTable.vue';
</script>

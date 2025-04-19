<template>
  <v-container>
    <v-card>
      <v-card-title>
        Breweries
      </v-card-title>
    </v-card>
    <v-card-text>
      <v-alert v-if="error" type="error">
        {{ error }}
      </v-alert>
      <v-data-table
        :headers="headers"
        :items="breweries"
        :loading="loading"
        item-value="id"
        :items-per-page="10"
        >
          <template v-slot:loading>
            <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
          </template>

          <template v-slot:no-data>
            No breweries found or failed to load data.
          </template>
      </v-data-table>
    </v-card-text>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import type { Ref } from 'vue';

interface Brewery {
  id: string;
  name: string;
  brewery_type: string;
  address_1: string | null;
  city: string | null;
  state: string | null;
  country: string | null;
}

const breweries: Ref<[Brewery]> = ref([]);
const loading: Ref<boolean> = ref(true);
const error: Ref<string | null> = ref(null);

const headers: any[] = [
  { title: 'Name', key: 'name', align: 'start', sortable: true },
  { title: 'Type', key: 'brewery_type', sortable: true },
  { title: 'City', key: 'city', sortable: true },
  { title: 'State', key: 'state', sortable: true },
  { title: 'Country', key: 'country', sortable: true },
  { title: 'Address', key: 'address_1', sortable: false },
];

onMounted(() => {
  fetchBreweries();
});

async function fetchBreweries() {
  loading.value = true;
  error.value = null;
  try {
    const response = await fetch('http://localhost:5000/breweries');
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'HTTP error! status: ' + response.status);
    }
    const data = await response.json();
    breweries.value = data.filter((b: Brewery) => b && b.id && b.name && b.brewery_type);
  } catch (err: any) {
    console.error('Failed to fetch breweries:', err);
    error.value = 'Failed to load breweries: ' + (err.message || 'Unknown error');
    breweries.value = [];
  } finally {
    loading.value = false;
    console.log('Loading finished, breweries fetched:', breweries.value);
  }
}

</script>
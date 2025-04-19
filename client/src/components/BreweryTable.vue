<template>
  <v-container>
    <v-card>
      <v-card-title>
        Breweries
        <v-row align="center" class="mb-4" dense>
          <v-col cols="12" sm="4">
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search Breweries"
              single-line
              hide-details
              density="compact"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-title>
    </v-card>
    <v-card-text>
      <v-alert v-if="error" type="error">
        {{ error }}
      </v-alert>
      <v-data-table
        :headers="headers"
        :items="filteredBreweries"
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
const search: Ref<string> = ref('');

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

const filteredBreweries = computed(() => {
  if (!search.value) {
    return breweries.value;
  }
  const searchTerm = search.value.toLowerCase();
  return breweries.value.filter(brewery => {
    return (
      brewery.name.toLowerCase().includes(searchTerm) ||
      brewery.brewery_type.toLowerCase().includes(searchTerm) ||
      (brewery.city && brewery.city.toLowerCase().includes(searchTerm)) ||
      (brewery.state && brewery.state.toLowerCase().includes(searchTerm)) ||
      (brewery.country && brewery.country.toLowerCase().includes(searchTerm)) ||
      (brewery.address_1 && brewery.address_1.toLowerCase().includes(searchTerm))
    );
  });
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
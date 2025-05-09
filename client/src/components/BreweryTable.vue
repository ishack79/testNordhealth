<template>
  <v-container>
    <v-card>
      <v-card-title>
        Breweries
        <v-row align="center" class="mb-4" dense>
          <v-col cols="12" sm="6">
             <v-select
                v-model="groupBy"
                :items="groupingOptions"
                label="Group By"
                item-title="title"
                item-value="key"
                density="compact"
                hide-details
                clearable
              ></v-select>
          </v-col>
          <v-col cols="12" sm="6">
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

      <GroupedPieChart
          v-if="groupBy"
          :chart-data="chartData"
          :chart-options="chartOptions"
      />
      
      <v-data-table
        :headers="headers"
        :items="filteredBreweries"
        :loading="loading"
        item-value="id"
        :items-per-page="10"
        :group-by="groupBy ? [{ key: groupBy, order: 'asc' }] : []"
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
import GroupedPieChart from '@/components/GroupedPieChart.vue';
import type { ChartData, ChartOptions } from 'chart.js';

interface Brewery {
  id: string;
  name: string;
  brewery_type: string;
  address_1: string | null;
  city: string | null;
  state: string | null;
  country: string | null;
}

const breweries: Ref<Brewery[]> = ref([]);
const loading: Ref<boolean> = ref(true);
const error: Ref<string | null> = ref(null);
const search: Ref<string> = ref('');
const groupBy: Ref<keyof Brewery | null> = ref(null);

const headers: any[] = [
  { title: 'Name', key: 'name', align: 'start', sortable: true },
  { title: 'Type', key: 'brewery_type', sortable: true },
  { title: 'City', key: 'city', sortable: true },
  { title: 'State', key: 'state', sortable: true },
  { title: 'Country', key: 'country', sortable: true },
  { title: 'Address', key: 'address_1', sortable: false },
];

const groupingOptions = [
  { title: 'Type', key: 'brewery_type' },
  { title: 'Country', key: 'country' },
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
    const response = await fetch('/breweries');
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

const chartData = computed<ChartData<'pie'>>(() => {
  const data: ChartData<'pie'> = {
    labels: [],
    datasets: [
      {
        backgroundColor: [
          '#41B883', '#E46651', '#00D8FF', '#DD1B16', '#FFC107', '#3F51B5'
        ],
        data: []
      }
    ]
  };

  if (!groupBy.value || filteredBreweries.value.length === 0) {
    return data;
  }

  const groupKey = groupBy.value;
  const counts: { [key: string]: number } = {};

  filteredBreweries.value.forEach(brewery => {
    const value = brewery[groupKey];
    const key = value === null ? 'N/A' : String(value);
    counts[key] = (counts[key] || 0) + 1;
  });

  const sortedLabels = Object.keys(counts).sort();

  data.labels = sortedLabels;
  data.datasets[0].data = sortedLabels.map(label => counts[label]);

  return data;
});

const chartOptions = computed<ChartOptions<'pie'>>(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    }
  }
}));

</script>
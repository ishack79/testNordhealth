<template>
    <div style="height: 400px; position: relative;">
      <Pie
        :data="chartData"
        :options="chartOptions"
      />
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineProps } from 'vue';
  import { Pie } from 'vue-chartjs';
  import {
    Chart as ChartJS,
    Tooltip,
    Legend,
    ArcElement,
    type ChartData,
    type ChartOptions
  } from 'chart.js';
  
  ChartJS.register(Tooltip, Legend, ArcElement);
  
  interface Props {
    chartData: ChartData<'pie'>;
    chartOptions: ChartOptions<'pie'>;
  }
  
  defineProps<Props>();
  </script>

<template>
  <div class="container mx-auto p-4">
    <h2 class="text-3xl font-semibold mb-6">Runs</h2>
    <!-- Display loading message if runs are being fetched -->
    <div v-if="loading" class="text-lg text-gray-700 mb-6">Loading runs...</div>
    <div v-else>
      <div v-for="run in runs" :key="run.run_id" class="mb-8">
        <div class="p-6 rounded-lg shadow-lg transition-shadow duration-300"
             :class="{'bg-green-100 border border-green-500': run.status === 'FINISHED', 'bg-red-100 border border-red-500': run.status === 'FAILED'}">
             <p class="text-gray-700 mb-1"><strong>Experiment Name:</strong> {{ run['params.experiment_name'] }}</p>
          <p class="text-gray-700 mb-1"><strong>Status:</strong> {{ run.status }}</p>
          <p class="text-gray-700 mb-1"><strong>Start Time:</strong> {{ formatDate(run.start_time) }}</p>
          <p class="text-gray-700 mb-1"><strong>MAE:</strong> {{ run['metrics.mae'] }}</p>
          <p class="text-gray-700 mb-1"><strong>MSE:</strong> {{ run['metrics.mse'] }}</p>
          <p class="text-gray-700 mb-1"><strong>R2:</strong> {{ run['metrics.r2'] }}</p>
          <p class="text-gray-700 mb-1"><strong>N Estimators:</strong> {{ run['params.n_estimators'] }}</p>
          <p class="text-gray-700 mb-1"><strong>Random State:</strong> {{ run['params.random_state'] }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      runs: [],
      loading: false,
      backendURL: process.env.VUE_APP_BACKEND_URL
    };
  },
  mounted() {
    this.fetchRuns();
  },
  methods: {
    async fetchRuns() {
      try {
        this.loading = true;
        const response = await fetch(`${this.backendURL}/runs`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.runs = await response.json();
      } catch (error) {
        console.error('Error fetching runs:', error);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toUTCString();
    }
  }
};
</script>

<style>
@import 'tailwindcss/tailwind.css';
</style>

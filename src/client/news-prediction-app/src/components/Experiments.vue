<template>
  <div class="container mx-auto p-4">
    <h2 class="text-3xl font-semibold mb-6">Experiments</h2>
    <!-- Display loading message if experiments are being fetched -->
    <div v-if="loading" class="text-lg text-gray-700 mb-6">Loading experiments...</div>
    <ul class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <li v-for="experiment in experiments" :key="experiment.experiment_id"
          class="p-6 rounded-lg shadow-lg transition-shadow duration-300"
          :class="{ 'bg-yellow-100 border border-yellow-500': experiment.lifecycle_stage === 'Production', 'bg-white': experiment.lifecycle_stage !== 'Production' }">
        <h3 class="text-xl font-semibold mb-2">{{ experiment.name }}</h3>
        <p class="text-gray-700 mb-1"><strong>ID:</strong> {{ experiment.experiment_id }}</p>
        <p class="text-gray-700"><strong>Stage:</strong> {{ experiment.lifecycle_stage }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      experiments: [],
      loading: false,
      backendURL: process.env.VUE_APP_BACKEND_URL
    };
  },
  mounted() {
    this.fetchExperiments();
  },
  methods: {
    async fetchExperiments() {
      try {
        this.loading = true;
        const response = await fetch(`${this.backendURL}/experiments`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.experiments = await response.json();
      } catch (error) {
        console.error('Error fetching experiments:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

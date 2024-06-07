<template>
  <div>
    <h2 class="text-3xl font-semibold mb-6">Runs</h2>
    <!-- Display loading message if results are being fetched -->
    <div v-if="loading" class="text-lg text-gray-700 mb-6">Loading testing results...</div>
    <div v-else>
      <div v-for="(result, index) in results" :key="index" class="mb-4">
        <div class="p-6 rounded-lg shadow-lg transition-shadow duration-300" :class="getResultCardColor(result)">
          <div v-if="result.summary">
            <p class="text-lg font-semibold mb-2">Summary</p>
            <p class="text-gray-700"><strong>All Passed:</strong> {{ result.summary.all_passed ? 'Yes' : 'No' }}</p>
            <p class="text-gray-700"><strong>Total Tests:</strong> {{ result.summary.total_tests }}</p>
            <p class="text-gray-700"><strong>Success Tests:</strong> {{ result.summary.success_tests }}</p>
            <p class="text-gray-700"><strong>Failed Tests:</strong> {{ result.summary.failed_tests }}</p>
          </div>
          <div v-if="result.tests">
            <p class="text-gray-700"><strong>Date and time:</strong> {{ result.timestamp }}</p>
            <p class="text-lg font-semibold mt-4 mb-2">Tests</p>
            <div v-for="(test, idx) in result.tests" :key="idx">
              <p class="text-gray-700"><strong>Name:</strong> {{ test.name }}</p>
              <p class="text-gray-700"><strong>Description:</strong> {{ test.description }}</p>
              <p class="text-gray-700"><strong>Group:</strong> {{ test.group }}</p>
              <p class="text-gray-700"><strong>Status:</strong> {{ test.status }}</p>
              <p class="text-gray-700"><strong>Parameters:</strong> {{ JSON.stringify(test.parameters) }}</p>
              <hr class="my-2 border-gray-200">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      results: [],
      loading: false, // loading state
      backendURL: process.env.VUE_APP_BACKEND_URL
    };
  },
  mounted() {
    this.fetchResults();
  },
  methods: {
    async fetchResults() {
      try {
        this.loading = true; // Start loading
        const response = await fetch(`${this.backendURL}/testing`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.results = await response.json();
      } catch (error) {
        console.error('Error fetching testing results:', error);
      } finally {
        this.loading = false; // Done loading
      }
    },
    getResultCardColor(result) {
      if (!result.summary || !result.summary.all_passed) return 'bg-white';
      return result.summary.all_passed ? 'bg-green-100 border border-green-500' : 'bg-red-100 border border-red-500';
    }
  }
};
</script>

<style>
@import 'tailwindcss/tailwind.css';
</style>

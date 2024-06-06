<template>
  <div>
    <h2>Testing Results</h2>
    <pre>{{ results }}</pre>
  </div>
</template>

<script>
export default {
  data() {
    return {
      results: null,
      backendURL: process.env.VUE_APP_BACKEND_URL
    };
  },
  mounted() {
    this.fetchResults();
  },
  methods: {
    async fetchResults() {
      try {
        const response = await fetch(`${this.backendURL}/testing`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.results = await response.json();
      } catch (error) {
        console.error('Error fetching testing results:', error);
      }
    }
  }
};
</script>

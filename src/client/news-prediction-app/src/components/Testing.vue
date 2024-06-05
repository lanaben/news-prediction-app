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
      results: null
    };
  },
  mounted() {
    this.fetchResults();
  },
  methods: {
    async fetchResults() {
      try {
        const response = await fetch('http://localhost:5000/testing');
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

<template>
  <div>
    <h2>Runs</h2>
    <ul>
      <li v-for="run in runs" :key="run.run_id">
        {{ run.run_id }} - Experiment: {{ run.experiment_id }} - Status: {{ run.status }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      runs: []
    };
  },
  mounted() {
    this.fetchRuns();
  },
  methods: {
    async fetchRuns() {
      try {
        const response = await fetch('http://localhost:5000/runs');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.runs = await response.json();
      } catch (error) {
        console.error('Error fetching runs:', error);
      }
    }
  }
};
</script>

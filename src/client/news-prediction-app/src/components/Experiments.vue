<template>
  <div>
    <h2>Experiments</h2>
    <ul>
      <li v-for="experiment in experiments" :key="experiment.experiment_id">
        {{ experiment.name }} - ID: {{ experiment.experiment_id }} - Stage: {{ experiment.lifecycle_stage }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      experiments: []
    };
  },
  mounted() {
    this.fetchExperiments();
  },
  methods: {
    async fetchExperiments() {
      try {
        const response = await fetch('http://localhost:5000/experiments');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.experiments = await response.json();
      } catch (error) {
        console.error('Error fetching experiments:', error);
      }
    }
  }
};
</script>

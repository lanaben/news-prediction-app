<template>
  <div>
    <h2>Models</h2>
    <ul>
      <li v-for="model in models" :key="model.version">
        {{ model.name }} - Version: {{ model.version }} - Stage: {{ model.current_stage }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      models: []
    };
  },
  mounted() {
    this.fetchModels();
  },
  methods: {
    async fetchModels() {
      try {
        const response = await fetch('http://localhost:5000/models');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.models = await response.json();
      } catch (error) {
        console.error('Error fetching models:', error);
      }
    }
  }
};
</script>

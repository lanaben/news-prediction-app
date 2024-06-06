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
      models: [],
      backendURL: process.env.VUE_APP_BACKEND_URL
    };
  },
  mounted() {
    this.fetchModels();
  },
  methods: {
    async fetchModels() {
      try {
        const response = await fetch(`${this.backendURL}/models`);
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

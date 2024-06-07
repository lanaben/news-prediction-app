<template>
  <div class="container mx-auto p-4">
    <h2 class="text-3xl font-semibold mb-6">Models</h2>
    <div v-if="loading" class="text-lg text-gray-700 mb-6">Loading models...</div>
    <div v-else>
      <div v-for="(models, name) in groupedModels" :key="name" class="mb-8">
        <h3 class="text-2xl font-semibold mb-4">{{ name }}</h3>
        <ul class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <li v-for="model in models" :key="model.version"
              :class="['p-6 rounded-lg shadow-lg transition-shadow duration-300', model.current_stage === 'Production' ? 'bg-yellow-100 border border-yellow-500' : 'bg-white']">
            <p class="text-gray-700 mb-1"><strong>Version:</strong> {{ model.version }}</p>
            <p class="text-gray-700"><strong>Stage:</strong> {{ model.current_stage }}</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      models: [],
      loading: false,
      backendURL: process.env.VUE_APP_BACKEND_URL
    };
  },
  mounted() {
    this.fetchModels();
  },
  methods: {
    async fetchModels() {
      try {
        this.loading = true;
        const response = await fetch(`${this.backendURL}/models`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.models = await response.json();
      } catch (error) {
        console.error('Error fetching models:', error);
      } finally {
        this.loading = false;
      }
    }
  },
  computed: {
    groupedModels() {
      return this.models.reduce((acc, model) => {
        if (!acc[model.name]) {
          acc[model.name] = [];
        }
        acc[model.name].push(model);
        return acc;
      }, {});
    }
  }
};
</script>

<style>
@import 'tailwindcss/tailwind.css';
</style>

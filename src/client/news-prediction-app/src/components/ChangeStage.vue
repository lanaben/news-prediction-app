<template>
  <div class="container mx-auto p-4">
    <h2 class="text-3xl font-semibold mb-6">Change Model Stage</h2>
    <form @submit.prevent="submitForm" class="bg-white p-6 rounded-lg shadow-lg">
      <div class="form-group mb-4">
        <label for="model_name" class="block mb-2 text-lg font-medium text-gray-700">Model Name:</label>
        <input type="text" v-model="form.model_name" class="form-input w-full" required />
      </div>
      <div class="form-group mb-4">
        <label for="version" class="block mb-2 text-lg font-medium text-gray-700">Version:</label>
        <input type="text" v-model="form.version" class="form-input w-full" required />
      </div>
      <div class="form-group mb-6">
        <label for="new_stage" class="block mb-2 text-lg font-medium text-gray-700">New Stage:</label>
        <select v-model="form.new_stage" class="form-select w-full" required>
          <option value="">Select a stage</option>
          <option value="None">None</option>
          <option value="Staging">Staging</option>
          <option value="Production">Production</option>
          <option value="Archived">Archived</option>
        </select>
      </div>
      <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" :disabled="loading">
        <span v-if="!loading">Change Stage</span>
        <span v-else>Loading...</span>
      </button>
    </form>
    <div v-if="message" class="mt-4 text-lg text-green-700">{{ message }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        model_name: '',
        version: '',
        new_stage: ''
      },
      message: null,
      loading: false, // loading state
      backendURL: process.env.VUE_APP_BACKEND_URL
    };
  },
  methods: {
    async submitForm() {
      try {
        this.loading = true; // Start loading
        const response = await fetch(`${this.backendURL}/change_model_stage`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.message = data.message;
      } catch (error) {
        console.error('Error changing model stage:', error);
        this.message = 'Error changing model stage';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style>
@import 'tailwindcss/tailwind.css';

.form-group {
  margin-bottom: 1.5rem;
}

.form-input, .form-select {
  display: block;
  width: 100%;
  padding: 0.75rem;
  border-radius: 0.375rem;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.form-input:focus, .form-select:focus {
  border-color: #007bff;
  outline: none;
}
</style>

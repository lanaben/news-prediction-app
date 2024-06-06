<template>
  <div>
    <h2>Change</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="model_name">Model Name:</label>
        <input type="text" v-model="form.model_name" required />
      </div>
      <div class="form-group">
        <label for="version">Version:</label>
        <input type="text" v-model="form.version" required />
      </div>
      <div class="form-group">
        <label for="new_stage">New Stage:</label>
        <input type="text" v-model="form.new_stage" required />
      </div>
      <button type="submit">Change Stage</button>
    </form>
    <div v-if="message">{{ message }}</div>
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
      backendURL: process.env.VUE_APP_BACKEND_URL
    };
  },
  methods: {
    async submitForm() {
      try {
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
      }
    }
  }
};
</script>

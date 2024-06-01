<template>
  <div class="container">
    <h1 class="title">News Article Prediction</h1>
    <form @submit.prevent="submitForm" class="form">
      <div class="form-group">
        <label for="DateTime">Date and Time</label>
        <input type="datetime-local" v-model="form.DateTime" required />
      </div>
      <div class="form-group">
        <label for="Title">Title</label>
        <input type="text" v-model="form.Title" required />
      </div>
      <div class="form-group">
        <label for="Categories">Categories</label>
        <input type="text" v-model="form.Categories" required />
      </div>
      <div class="form-group">
        <label for="Sentiment">Sentiment</label>
        <input type="text" v-model="form.Sentiment" required />
      </div>
      <div class="form-group">
        <label for="Keywords">Keywords</label>
        <input type="text" v-model="form.Keywords" required />
      </div>
      <button type="submit" class="button">Predict</button>
    </form>
    <div v-if="prediction !== null" class="result">
      <h2>Prediction Result</h2>
      <p>{{ prediction }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      form: {
        DateTime: '',
        Title: '',
        Categories: '',
        Sentiment: '',
        Keywords: ''
      },
      prediction: null
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('http://localhost:5000/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        });
        const data = await response.json();
        this.prediction = data.prediction;
      } catch (error) {
        console.error('There was an error making the request:', error);
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

.form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.button {
  padding: 10px;
  font-size: 18px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button:hover {
  background-color: #0056b3;
}

.result {
  margin-top: 20px;
  padding: 20px;
  border-top: 1px solid #ccc;
}

.result h2 {
  margin-bottom: 10px;
}

.result p {
  font-size: 18px;
}
</style>

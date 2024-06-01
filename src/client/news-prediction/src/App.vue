<template>
  <div class="container">
    <h1 class="title">JOURNALISTS HELPER</h1>
    <div v-if="articles.length" class="articles">
      <h2>Popular Articles In Technology</h2>
      <div class="article-list">
        <div v-for="article in articles" :key="article.id" class="article-item">
          <h3>{{ article.Title }}</h3>
          <p><strong>Categories:</strong> {{ article.Categories }}</p>
          <p><strong>Sentiment:</strong> {{ article.Sentiment }}</p>
          <p><strong>DateTime:</strong> {{ article.DateTime }}</p>
          <p><strong>Keywords:</strong> {{ article.Keywords }}</p>
        </div>
      </div>
    </div>
    <div class="form-container">
      <h1>iS MY ARTICLE GOING TO BE RELEVANT?</h1>
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
    </div>
    <div v-if="prediction !== null" class="result">
      <h2>Prediction Result</h2>
      <p>{{ prediction }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const form = ref({
  DateTime: '',
  Title: '',
  Categories: '',
  Sentiment: '',
  Keywords: ''
});

const articles = ref([]);
const prediction = ref(null);

const fetchArticles = async () => {
  try {
    const response = await fetch('http://localhost:5000/articles');
    const data = await response.json();
    articles.value = data;
  } catch (error) {
    console.error('There was an error fetching the articles:', error);
  }
};

const submitForm = async () => {
  try {
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form.value)
    });
    const data = await response.json();
    prediction.value = data.prediction;
  } catch (error) {
    console.error('There was an error making the request:', error);
  }
};

onMounted(fetchArticles);
</script>

<style scoped>
.container {
}

.title {
  text-align: center;
  color: #007bff;
}

.articles {
  margin-bottom: 30px;
}

.articles h2 {
  color: #007bff;
}

.article-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.article-item {
  width: 100%;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.form-container {
  text-align: center;
}

.form {
  display: inline-block;
  text-align: left;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.button {
  padding: 10px 20px;
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
  color: #007bff;
}

.result p {
  font-size: 18px;
  color: #555;
}
</style>

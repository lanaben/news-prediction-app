<template>
  <div class="container">
    <div class="articles-section">
      <h2>Latest Articles</h2>
      <div class="articles">
        <div v-for="article in articles" :key="article.id" class="article">
          <h3>{{ article.Title }}</h3>
          <p>{{ article.DateTime }}</p>
          <p>{{ article.Categories }}</p>
          <p>{{ article.Sentiment }}</p>
          <p>{{ article.Keywords }}</p>
        </div>
      </div>
    </div>
    <div class="form-section">
      <h2>Predict News Outcome</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="DateTime">DateTime:</label>
          <input type="datetime-local" v-model="form.DateTime" required />
        </div>
        <div class="form-group">
          <label for="Title">Title:</label>
          <input type="text" v-model="form.Title" required />
        </div>
        <div class="form-group">
          <label for="Categories">Categories:</label>
          <input type="text" v-model="form.Categories" required />
        </div>
        <div class="form-group">
          <label for="Sentiment">Sentiment:</label>
          <input type="text" v-model="form.Sentiment" required />
        </div>
        <div class="form-group">
          <label for="Keywords">Keywords:</label>
          <input type="text" v-model="form.Keywords" required />
        </div>
        <button type="submit">Predict</button>
      </form>
      <div v-if="prediction">
        <h3>Prediction Result</h3>
        <p>{{ prediction }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      articles: [],
      form: {
        DateTime: '',
        Title: '',
        Categories: '',
        Sentiment: '',
        Keywords: ''
      },
      prediction: null,
      backendURL: process.env.VUE_APP_BACKEND_URL
    };
  },
  mounted() {
    this.fetchArticles();
  },
  methods: {
    async fetchArticles() {
      try {
        const response = await fetch(`${this.backendURL}/articles`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.articles = await response.json();
      } catch (error) {
        console.error('Error fetching articles:', error);
      }
    },
    async submitForm() {
      try {
        const response = await fetch(`${this.backendURL}/predict`, {
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
        this.prediction = data.prediction;
      } catch (error) {
        console.error('Error making prediction:', error);
      }
    }
  }
};
</script>

<style scoped>
.container {
  width: 80%;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.articles-section {
  margin-bottom: 50px;
}

.articles {
  display: flex;
  justify-content: space-between;
}

.article {
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
  width: 18%;
}

.form-section {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #0056b3;
}
</style>

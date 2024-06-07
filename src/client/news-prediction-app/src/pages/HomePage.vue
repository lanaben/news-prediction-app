<template>
  <div class="container mx-auto p-6 font-sans max-w-1500">

    <button @click="goToAdminPage" class="absolute top-4 right-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
      Admin Console
    </button>

    <!-- Articles Section -->
    <div class="articles-section mb-12">
      <h2 class="text-3xl font-bold mb-6 text-center">News</h2>
      <div class="articles grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <div v-for="article in articles.slice(0, 5)" :key="article.id" class="article p-4 bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
          <h3 class="text-xl font-semibold mb-2">{{ article.Title }}</h3>
          <p class="text-gray-600">{{ formatDate(article.DateTime) }}</p>
          <p class="text-gray-600">{{ article.Categories }}</p>
          <p class="text-gray-600">Sentiment: {{ getSentimentLabel(article.Sentiment) }}</p>
          <p class="text-gray-600">Relevance: {{ article.Relevance }}</p>
        </div>
      </div>
    </div>

    <!-- Prediction Form Section -->
    <div class="form-section bg-gray-50 p-6 rounded-lg shadow-md">
      <h2 class="text-3xl font-bold mb-6 text-center">Predict News Outcome</h2>
      <form @submit.prevent="submitForm" class="space-y-4">
        <div class="form-group">
          <label for="DateTime" class="block text-gray-700">DateTime:</label>
          <input type="datetime-local" v-model="form.DateTime" required class="input-field" />
        </div>
        <div class="form-group">
          <label for="Title" class="block text-gray-700">Title:</label>
          <input type="text" v-model="form.Title" required class="input-field" />
        </div>
        <div class="form-group">
          <label for="Categories" class="block text-gray-700">Categories:</label>
          <select v-model="form.Categories" required class="input-field">
            <option disabled value="">Select a Category</option>
            <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="Sentiment" class="block text-gray-700">Sentiment (from -1 to 1, -1 meaning negative, 1 positive):</label>
          <input type="number" step="0.01" v-model="form.Sentiment" required class="input-field" />
        </div>
        <div class="form-group">
          <label for="Keywords" class="block text-gray-700">Keywords:</label>
          <input type="text" v-model="form.Keywords" required class="input-field" />
        </div>
        <button type="submit" class="submit-button">
          <span v-if="!predicting">Predict</span>
          <span v-else>Predicting...</span>
        </button>
      </form>

      <!-- Prediction Result -->
      <div v-if="prediction !== null" class="mt-6 p-4 bg-green-100 text-green-800 rounded-lg">
        <h3 class="text-xl font-semibold mb-2">Prediction Result</h3>
        <p>{{ prediction }}</p>
        <div v-if="prediction >= 1 && prediction <= 5" class="mt-4">
          <p>Your article may not attract much attention. Consider adding a more engaging title.</p>
        </div>
        <div v-else-if="prediction > 5 && prediction <= 10" class="mt-4">
          <p>Your article is likely to be popular! Make sure to promote it to reach a wider audience.</p>
        </div>
        <div v-else-if="prediction > 10" class="mt-4">
          <p>Your article is expected to be super popular! Get ready for a lot of attention.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      articles: [],
      categories: [
        "Home",
        "Computers",
        "Business",
        "Recreation",
        "Society",
        "Science",
        "Shopping",
        "Sports",
        "Arts",
        "Games",
        "Health"
      ],
      form: {
        DateTime: '',
        Title: '',
        Categories: '',
        Sentiment: '',
        Keywords: ''
      },
      prediction: null,
      predicting: false, // Flag to indicate if prediction is in progress
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
        this.predicting = true;
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
      } finally {
        this.predicting = false;
      }
    },
    formatDate(dateTime) {
      const date = new Date(dateTime);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    getSentimentLabel(sentiment) {
      if (sentiment <= -1) {
        return 'Negative';
      } else if (sentiment >= -0.3 && sentiment <= 0.3) {
        return 'Neutral';
      } else if (sentiment >= 0.3 && sentiment <= 1) {
        return 'Positive';
      } else {
        return 'Unknown';
      }
    },
    goToAdminPage() {
      // Redirect to /admin page
      this.$router.push('/admin');
    }
  }
};
</script>

<style scoped>
.input-field {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #CBD5E0;
  border-radius: 0.375rem;
  outline: none;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  border-color: #4C51BF;
}

.submit-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4299e1;
  color: #fff;
  border: none;
  border-radius: 0.375rem;
  outline: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #3182ce;
}
</style>

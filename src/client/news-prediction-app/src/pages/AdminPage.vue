<template>
  <div class="container">
    <div class="buttons">
      <button v-for="(btn, index) in buttons" :key="index" @click="currentView = btn">
        {{ btn }}
      </button>
    </div>
    <div class="content">
      <component :is="currentView"></component>
    </div>
  </div>
</template>

<script>
import {ref} from 'vue';
import Models from '../components/Models.vue';
import ChangeStage from '../components/ChangeStage.vue';
import Experiments from '../components/Experiments.vue';
import Runs from '../components/Runs.vue';
import Testing from '../components/Testing.vue';
import Validation from '../components/Validation.vue';

export default {
  setup() {
    const buttons = ['Models', 'ChangeStage', 'Experiments', 'Runs', 'Testing', 'Validation'];
    const currentView = ref('Models');

    return {
      buttons,
      currentView
    };
  },
  components: {
    Models,
    ChangeStage,
    Experiments,
    Runs,
    Testing,
    Validation
  }
};
</script>

<style scoped>
@import 'tailwindcss/tailwind.css';
.container {
  width: 80%;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
  margin-top: 20px;
}
.content {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 5px;
  min-height: 400px;
}
</style>

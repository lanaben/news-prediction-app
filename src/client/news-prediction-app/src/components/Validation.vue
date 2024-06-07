<template>
  <div>
    <h2>Validation Results</h2>
    <button><a :href="validationReportURL" download>Download Validation Report</a> </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      validationReportURL: `${process.env.VUE_APP_BACKEND_URL}/validation`
    };
  }
};
</script>

<style>
@import 'tailwindcss/tailwind.css';
</style>

<template>
  <div>
    <h2>Validation Results</h2>
    <a :href="validationReportURL" download>Download Validation Report</a>
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

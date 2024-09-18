<template>
  <div>
    <h1>Bienvenido al Panel Administrativo</h1>
    <Home />
  </div>
</template>

<script>

import Home from '../components/Home.vue';

export default {
  components:{ Home }
};
</script>

<style scoped>
h1 {
  font-size: 24px;
  font-weight: bold;
}
</style>

import { createStore } from 'vuex';

export default createStore({
  state: {
    user: null,
    products: [],
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setProducts(state, products) {
      state.products = products;
    },
  },
  actions: {
    login({ commit }, { email, token }) {
      localStorage.setItem('access_token', token);
    },
    fetchProducts({ commit }, products) {
      commit('setProducts', products);
    },
  },
  getters: {
    isAuthenticated(state) {
      return !!state.user;
    },
    userName(state) {
      return state.user ? state.user.nombre : 'Usuario';
    },
  },
});

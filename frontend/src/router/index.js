import { createRouter, createWebHistory } from 'vue-router'; 
import AdminLayout from '../components/AdminLayout.vue';
import HomeView from '../views/HomeView.vue';
import UsersView from '../views/UsersView.vue';
import ProductsView from '../views/ProductsView.vue';
import LoginView from '../views/LoginView.vue';
import { isAuthenticated } from '../utils/auth';

const routes = [
  {
    path: '/',
    redirect: '/home',
    component: AdminLayout,
    children: [
      {
        path: 'home',
        name: 'Home',
        component: HomeView,
        meta: { requiresAuth: true }
      },
      {
        path: 'users',
        name: 'Users',
        component: UsersView,
        meta: { requiresAuth: true }
      },
      {
        path: 'products',
        name: 'Products',
        component: ProductsView,
        meta: { requiresAuth: true }
      },
    ],
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/:catchAll(.*)',
    redirect: '/login'
  }
];

const router = createRouter({
  history: createWebHistory(), 
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = isAuthenticated();

  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login');
  } else if (to.path === '/login' && isLoggedIn) {
    next('/home');
  } else {
    next();
  }
});

export default router;

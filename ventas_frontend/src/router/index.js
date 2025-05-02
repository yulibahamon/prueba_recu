import { createRouter, createWebHistory } from 'vue-router';

// Importamos las vistas
const Dashboard = () => import('../views/Dashboard.vue');
const Sales = () => import('../views/Sales.vue');
const Statistics = () => import('../views/Statistics.vue');

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    alias: '/dashboard'
  },
  {
    path: '/sales',
    name: 'Sales',
    component: Sales
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: Statistics
  },
  // Redirigir rutas no encontradas al dashboard
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
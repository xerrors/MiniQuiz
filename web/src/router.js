import { createMemoryHistory, createRouter } from 'vue-router'
import HomeView from './views/HomeView.vue';
import QuizView from './views/QuizView.vue';
import Result from './components/Result.vue';

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView,
    meta: {
      isHome: true,
    },
  },
  {
    path: '/quiz',
    name: 'QuizView',
    component: QuizView,
  },
  {
    path: '/result',
    name: 'Result',
    component: Result,
  },
  {
    path: '/records',
    name: 'Records',
    component: () => import('./views/RecordsView.vue'),
  },
  {
    path: '/overall',
    name: 'Overall',
    component: () => import('./views/OverallView.vue'),
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('./views/AdminView.vue'),
    meta: {
      requiresAdmin: true,
    },
  }
];

const router = createRouter({
  history: createMemoryHistory(),
  routes,
});

export default router;

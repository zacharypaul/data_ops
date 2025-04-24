import { createRouter, createWebHistory } from 'vue-router'

import Dashboard from '../views/Dashboard.vue'
import Inventory from '../views/Inventory.vue'
import Observability from '../views/Observability.vue'
import BracketView from '../views/BracketView.vue'
import Costs from '../views/Costs.vue'
import MLOps from '../views/MLOps.vue'
import AIOps from '../views/AIOps.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/inventory',
    name: 'Inventory',
    component: Inventory
  },
  {
    path: '/observability',
    name: 'Observability',
    component: Observability
  },
  {
    path: '/bracket',
    name: 'DataPlatformBracket',
    component: BracketView
  },
  {
    path: '/costs',
    name: 'Costs',
    component: Costs
  },
  {
    path: '/mlops',
    name: 'MLOps',
    component: MLOps
  },
  {
    path: '/aiops',
    name: 'AIOps',
    component: AIOps
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 
<template>
  <v-app>
    <v-navigation-drawer
      app
      permanent
      dark
      width="200"
      color="#1E2130"
    >
      <v-list-item class="px-4 py-3">
        <v-list-item-content>
          <v-list-item-title class="text-h6 font-weight-medium white--text">
            <v-icon class="mr-2">mdi-chart-line</v-icon>
            VentaStats
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list
        dense
        nav
        class="py-0"
      >
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.to"
          exact
          link
          class="menu-item py-3"
          :class="{'selected-item': isCurrentRoute(item.to)}"
        >
          <div class="d-flex align-center">
            <v-icon class="ml-2 mr-3" :color="isCurrentRoute(item.to) ? '#7E84F3' : 'white'">{{ item.icon }}</v-icon>
            <span :class="{'purple--text': isCurrentRoute(item.to)}">{{ item.title }}</span>
          </div>
        </v-list-item>
      </v-list>
      
      <template v-slot:append>
        <v-list dense nav>
          <v-list-item exact link class="menu-item py-3" to="/">
            <div class="d-flex align-center">
              <v-icon class="ml-2 mr-3">mdi-cog</v-icon>
              <span>Inicio</span>
            </div>
          </v-list-item>
        </v-list>
      </template>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      menuItems: [
        { title: 'Dashboard', icon: 'mdi-view-dashboard-outline', to: '/dashboard', selected: true },
        { title: 'Ventas', icon: 'mdi-cart-outline', to: '/sales', selected: false },
        { title: 'Estadísticas', icon: 'mdi-chart-bar', to: '/statistics', selected: false }
      ]
    }
  },
  methods: {
    isCurrentRoute(route) {
      return this.$route.path === route;
    }
  }
}
</script>

<style scoped>
.v-application {
  font-family: 'Roboto', sans-serif;
}

.v-navigation-drawer {
  background-color: #1E2130 !important;
}

.selected-item {
  background-color: rgba(126, 132, 243, 0.1) !important;
  border-left: 3px solid #7E84F3;
}

.menu-item {
  margin-bottom: 5px;
  height: 44px !important;
}

.menu-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.d-flex.align-center {
  width: 100%;
}

.purple--text {
  color: #7E84F3 !important;
}
</style>
import { createStore } from 'vuex';

export default createStore({
  state: {
    // Estado global de la aplicación
    darkMode: false,
    sidebarOpen: true
  },
  getters: {
    // Getters para acceder al estado
    isDarkMode: state => state.darkMode,
    isSidebarOpen: state => state.sidebarOpen
  },
  mutations: {
    // Mutaciones para modificar el estado
    SET_DARK_MODE(state, value) {
      state.darkMode = value;
    },
    TOGGLE_SIDEBAR(state) {
      state.sidebarOpen = !state.sidebarOpen;
    }
  },
  actions: {
    // Acciones para ejecutar lógica de negocio
    setDarkMode({ commit }, value) {
      commit('SET_DARK_MODE', value);
    },
    toggleSidebar({ commit }) {
      commit('TOGGLE_SIDEBAR');
    }
  },
});
import { createApp, h } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import { DefaultApolloClient } from '@vue/apollo-composable';
import apolloClient from './apollo';

// Vuetify
import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import '@mdi/font/css/materialdesignicons.css';

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light'
  }
});

const app = createApp({
  setup() {
    return {
      // Proporcionar el cliente Apollo a la aplicación
    };
  },
  render: () => h(App),
});

// Proporcionar el cliente Apollo a nivel de aplicación
app.provide(DefaultApolloClient, apolloClient);

app.use(store)
   .use(router)
   .use(vuetify)
   .mount('#app');
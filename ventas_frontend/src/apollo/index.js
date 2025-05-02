import { ApolloClient, createHttpLink, InMemoryCache } from '@apollo/client/core';


// Definir la URL de tu API GraphQL
const httpLink = createHttpLink({
  uri: process.env.VUE_APP_API_URL// Ajusta la URL según tu configuración de Django definifa en .env
});

// Crear el cliente Apollo
const apolloClient = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
  defaultOptions: {
    query: {
      fetchPolicy: 'network-only', // No usar caché para consultas por defecto
    },
  },
});

export default apolloClient;
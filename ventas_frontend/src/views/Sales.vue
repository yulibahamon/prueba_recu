/**
 * @component SalesView
 * @description Componente para mostrar y gestionar la tabla de ventas.
 * Incluye funcionalidades de búsqueda, ordenamiento y formato de datos.
 */
<template>
  <div>
    <!-- Cabecera de la página -->
    <h1 class="text-h4 mb-4">Tabla de Ventas</h1>
    <p class="mb-6">Listado completo de productos vendidos y cantidad de veces vendido.</p>
    
    <!-- Tarjeta principal que contiene la tabla -->
    <v-card outlined>
      <!-- Barra superior con título y buscador -->
      <v-card-title class="d-flex align-center">
        Todas las Ventas ({{ salesData.length }} registros)
        <v-spacer></v-spacer>
        <!-- Campo de búsqueda -->
        <v-text-field
          v-model="search"
          label="Buscar" 
          single-line
          hide-details
          density="compact"
          class="mt-0 pt-0"
          style="max-width: 300px;"
        ></v-text-field>
      </v-card-title>
      
      <!-- Tabla de datos con soporte para ordenamiento y búsqueda -->
      <v-data-table
        :headers="headers"
        :items="salesData"
        :search="search"
        :loading="loading"
        loading-text="Cargando datos... Por favor, espere"
        class="elevation-1"
        :sort-by="[{ key: 'date', order: 'desc' }]"
      >
        <!-- Templates personalizados para formato de datos -->
        <template #[`item.date`]="props">
          {{ formatDate(props.item.date) }}
        </template>
        
        <template #[`item.product.price`]="props">
          {{ formatCurrency(props.item.product.price) }}
        </template>
        
        <template #[`item.totalAmount`]="props">
          {{ formatCurrency(props.item.totalAmount) }}
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { useQuery } from '@vue/apollo-composable';
import { ALL_SALES } from '../graphql/queries';
import moment from 'moment';

export default defineComponent({
  name: 'SalesView',
  setup() {
    // Referencias reactivas
    const salesData = ref([]); // Almacena los datos de ventas
    const search = ref(''); // Término de búsqueda
    
    // Definición de las columnas de la tabla
    const headers = ref([
      { title: 'Producto', key: 'product.name', sortable: true },
      { title: 'Cantidad', key: 'quantity', sortable: true },
      { title: 'Fecha', key: 'date', sortable: true },
      { title: 'Precio Unitario', key: 'product.price', sortable: true },
      { title: 'Total', key: 'totalAmount', sortable: true },
    ]);
    
    // Consulta GraphQL para obtener las ventas
    const { loading, onResult: onSalesResult } = useQuery(ALL_SALES);
    
    /**
     * Formatea una fecha a formato DD/MM/YYYY
     * @param {string} dateString - Fecha en formato ISO
     * @returns {string} Fecha formateada
     */
    const formatDate = (dateString) => {
      return dateString ? moment(dateString).format('DD/MM/YYYY') : '-';
    };
    
    /**
     * Formatea un valor numérico a formato de moneda
     * @param {number} value - Valor a formatear
     * @returns {string} Valor formateado como moneda
     */
    const formatCurrency = (value) => {
      return new Intl.NumberFormat('es-ES', { 
        style: 'currency', 
        currency: 'EUR',
        minimumFractionDigits: 2
      }).format(value);
    };
    
    // Manejador del resultado de la consulta GraphQL
    onSalesResult(result => {
      if (result.data && result.data.allSales) {
        salesData.value = result.data.allSales;
      }
    });
    
    // Exposición de propiedades y métodos al template
    return {
      salesData,
      headers,
      search,
      loading,
      formatDate,
      formatCurrency
    };
  }
});
</script>

<style scoped>
/* Estilo personalizado para los encabezados de la tabla */
.v-data-table ::v-deep th {
  font-weight: bold;
  background-color: #f5f5f5;
}
</style>
<template>
    <div>
      <h1 class="text-h4 mb-4">Dashboard de Resumen</h1>
      
      <v-row>
        <!-- Tarjetas de resumen -->
        <v-col cols="12" sm="6" md="3">
          <v-card class="mx-auto" max-width="344" outlined>
            <v-card-text>
              <p class="text-subtitle-1">Total de Ventas</p>
              <p class="text-h5" v-if="!loading">{{ summaryData.totalSales }}</p>
              <v-skeleton-loader v-else type="text"></v-skeleton-loader>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" sm="6" md="3">
          <v-card class="mx-auto" max-width="344" outlined>
            <v-card-text>
              <p class="text-subtitle-1">Cantidad Total Vendida</p>
              <p class="text-h5" v-if="!loading">{{ formatCurrency(summaryData.totalRevenue) }}</p>
              <v-skeleton-loader v-else type="text"></v-skeleton-loader>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" sm="6" md="3">
          <v-card class="mx-auto" max-width="344" outlined>
            <v-card-text>
              <p class="text-subtitle-1">Promedio de Venta</p>
              <p class="text-h5" v-if="!loading">{{ formatCurrency(summaryData.medianSale) }}</p>
              <v-skeleton-loader v-else type="text"></v-skeleton-loader>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" sm="6" md="3">
          <v-card class="mx-auto" max-width="344" outlined>
            <v-card-text>
              <p class="text-subtitle-1">Mediana de Venta</p>
              <p class="text-h5" v-if="!loading">{{ formatCurrency(summaryData.medianSale) }}</p>
              <v-skeleton-loader v-else type="text"></v-skeleton-loader>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
  
      <v-row class="mt-6">
        <!-- Sección superior del cliente -->
        <v-col cols="12" sm="6">
          <v-card outlined>
            <v-card-title>Cliente Top</v-card-title>
            <v-card-text v-if="!loadingTopCustomer">
              <p><strong>Nombre:</strong> {{ topCustomer.customer.name }}</p>
              <p><strong>Total de Compras:</strong> {{ topCustomer.totalPurchases }}</p>
              <p><strong>Cantidad Total:</strong> {{ formatCurrency(topCustomer.totalSpent) }}</p>
            </v-card-text>
            <v-skeleton-loader v-else type="list-item-three-line"></v-skeleton-loader>
          </v-card>
        </v-col>
        
        <!-- Sección superior del producto -->
        <v-col cols="12" sm="6">
          <v-card outlined>
            <v-card-title>Producto Top</v-card-title>
            <v-card-text v-if="!loadingTopProduct">
              <p><strong>Nombre:</strong> {{ topProduct.product.name }}</p>
              <p><strong>Total de Ventas:</strong> {{ topProduct.totalSales }}</p>
              <p><strong>Cantidad Total:</strong> {{ formatCurrency(topProduct.totalRevenue) }}</p>
            </v-card-text>
            <v-skeleton-loader v-else type="list-item-three-line"></v-skeleton-loader>
          </v-card>
        </v-col>
      </v-row>
  
      <v-row class="mt-6">
        <!-- Tabla de ventas -->
        <v-col cols="12">
          <v-card outlined>
            <v-card-title class="d-flex align-center">
              Resumen de Ventas por Producto
              <v-spacer></v-spacer>
              <v-text-field
                v-model="search"
                label="Buscar"
                single-line
                hide-details
              ></v-text-field>
            </v-card-title>
            
            <v-data-table
              :headers="headers"
              :items="productSalesData"
              :search="search"
              :loading="loadingSalesStats"
              loading-text="Cargando datos... Por favor, espere"
              class="elevation-1"
            >

            <!-- Template personalizado para la columna de ingresos totales -->
            <template #[`item.totalRevenue`]="{ item }">
              {{ formatCurrency(item.totalRevenue) }}
            </template>
          </v-data-table>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, reactive } from 'vue';
  import { useQuery } from '@vue/apollo-composable';
  import { SALES_SUMMARY, TOP_CUSTOMER, TOP_PRODUCT, PRODUCT_SALES_STATS } from '../graphql/queries';
  
  export default defineComponent({
    name: 'DashboardView',
    setup() {
      // Estado para los datos
      const summaryData = reactive({
        totalSales: 0,
        totalQuantitySold: 0,
        averageSalePerProduct: 0,
        medianSale: 0,
        modeSale: 0
      });
      
      const topCustomer = reactive({
        customer: {
          id: '',
          name: ''
        },
        totalPurchases: 0,
        totalQuantity: 0,
        totalSpent: 0,
      });
      
      const topProduct = reactive({
        productId: '',
        productName: '',
        product: {
          id: '',
          name: '',
          price: ''
        },
        totalSales: 0,
        totalQuantity: 0,
        totalRevenue: 0,
      });
      
      const productSalesData = ref([]);
      const search = ref('');
      
      // Encabezados para la tabla
      const headers = [
        { title: 'Producto', key: 'productName' },
        { title: 'Total de Ventas', key: 'totalSales' },
        { title: 'Cantidad Vendida', key: 'totalRevenue' }
      ];
      
      // Consultas GraphQL
      const { loading, onResult: onSummaryResult } = useQuery(SALES_SUMMARY);
      const { loading: loadingTopCustomer, onResult: onCustomerResult } = useQuery(TOP_CUSTOMER);
      const { loading: loadingTopProduct, onResult: onProductResult } = useQuery(TOP_PRODUCT);
      const { loading: loadingSalesStats, onResult: onSalesStatsResult } = useQuery(PRODUCT_SALES_STATS);
      
      // Manejar resultados
      onSummaryResult(result => {
        if (result.data && result.data.salesSummary) {
          Object.assign(summaryData, result.data.salesSummary);
        }
      });
      
      onCustomerResult(result => {
        if (result.data && result.data.topCustomer) {
          Object.assign(topCustomer, result.data.topCustomer);
        }
      });
      
      
      onProductResult(result => {
        if (result.data && result.data.topProduct) {
          Object.assign(topProduct, result.data.topProduct);
        }
      });
      
      onSalesStatsResult(result => {
        if (result.data && result.data.productSalesStats) {
          productSalesData.value = result.data.productSalesStats;
        }
      });
      
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

      return {
        summaryData,
        topCustomer,
        topProduct,
        productSalesData,
        headers,
        search,
        loading,
        loadingTopCustomer,
        loadingTopProduct,
        loadingSalesStats,
        formatCurrency
      };
    }
  });
  </script>
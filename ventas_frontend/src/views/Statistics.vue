<template>
  <div>
    <h1 class="text-h4 mb-4">Estadísticas de Ventas</h1>
    
    <v-row>
      <!-- Gráfico de línea: Ventas mensuales -->
      <v-col cols="12">
        <v-card outlined>
          <v-card-title>Ventas Mensuales</v-card-title>
          <v-card-text>
            <line-chart v-if="!loading && monthlySalesChartData.labels.length > 0" :chart-data="monthlySalesChartData" />
            <v-skeleton-loader v-else type="image" height="400"></v-skeleton-loader>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-6">
      <!-- Gráfico de barras por producto -->
      <v-col cols="12" md="6">
        <v-card outlined>
          <v-card-title>Productos por Ventas Totales</v-card-title>
          <v-card-text>
            <bar-chart v-if="!loadingSalesStats && salesChartData.labels.length > 0" :chart-data="salesChartData" :options="salesChartOptions" />
            <v-skeleton-loader v-else type="image" height="300"></v-skeleton-loader>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Indicadores estadísticos -->
      <v-col cols="12" md="6">
        <v-card outlined>
          <v-card-title>Métricas Estadísticas</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Producto Más Vendido:</v-list-item-title>
                  <v-list-item-subtitle v-if="summaryData.modeProduct">{{ summaryData.modeProduct.name }}</v-list-item-subtitle>
                  <v-list-item-subtitle v-else>No disponible</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Promedio de Venta:</v-list-item-title>
                  <v-list-item-subtitle>{{ formatCurrency(summaryData.averageSale) }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Mediana de Venta:</v-list-item-title>
                  <v-list-item-subtitle>{{ formatCurrency(summaryData.medianSale) }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Total de Ventas:</v-list-item-title>
                  <v-list-item-subtitle>{{ summaryData.totalSales }} transacciones</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Ingresos Totales:</v-list-item-title>
                  <v-list-item-subtitle>{{ formatCurrency(summaryData.totalRevenue) }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item v-if="summaryData.topCustomer">
                <v-list-item-content>
                  <v-list-item-title>Cliente Principal:</v-list-item-title>
                  <v-list-item-subtitle>{{ summaryData.topCustomer.name }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  import { defineComponent, ref, reactive, computed } from 'vue';
  import { useQuery } from '@vue/apollo-composable';
  import { MONTHLY_SALES, PRODUCT_SALES_STATS, SALES_SUMMARY } from '../graphql/queries';
  import LineChart from '../components/charts/LineChart.vue';
  import BarChart from '../components/charts/BarChart.vue';

  export default defineComponent({
    name: 'StatisticsView',
    components: {
      LineChart,
      BarChart
    },
    setup() {
      // Estado para los datos
      const monthlySalesData = ref([]);
      const productSalesData = ref([]);
      const summaryData = reactive({
        modeProduct: null,
        averageSale: 0,
        medianSale: 0,
        totalRevenue: 0,
        totalSales: 0,
        topCustomer: null
      });
      
      // Consultas GraphQL
      const { loading, onResult: onMonthlySalesResult } = useQuery(MONTHLY_SALES);
      const { loading: loadingSalesStats, onResult: onSalesStatsResult } = useQuery(PRODUCT_SALES_STATS);
      const { loading: loadingSummary, onResult: onSummaryResult } = useQuery(SALES_SUMMARY);
      
      // Manejar resultados de consultas
      onMonthlySalesResult(result => {
        if (result.data && result.data.monthlySales) {
          // Convertir los datos y asegurar que cada objeto tenga una propiedad year
          monthlySalesData.value = [...result.data.monthlySales].map(item => {
            // Extraer el año y mes del campo month (asumiendo formato "YYYY-MM")
            const [year, monthNum] = (item.month || '').split('-');
            return {
              year: year || new Date().getFullYear().toString(),
              month: monthNum || '1',
              salesCount: item.salesCount || 0,
              totalUnitsSold: item.totalUnitsSold || 0,
              totalRevenue: item.totalRevenue || 0
            };
          }).sort((a, b) => {
            // Ordenar por año y mes
            if (a.year !== b.year) return parseInt(a.year) - parseInt(b.year);
            return parseInt(a.month) - parseInt(b.month);
          });
          
          console.log('Datos de ventas mensuales procesados:', monthlySalesData.value);
        }
      });
      
      onSalesStatsResult(result => {
        if (result.data && result.data.productSalesStats) {
          productSalesData.value = result.data.productSalesStats;
          console.log('Datos de estadísticas de ventas:', productSalesData.value);
        }
      });
      
      onSummaryResult(result => {
        if (result.data && result.data.salesSummary) {
          // Copiar los datos directamente del resultado al estado reactivo
          Object.assign(summaryData, result.data.salesSummary);
          console.log('Datos de resumen:', summaryData);
        }
      });
      
      // Formatear moneda
      const formatCurrency = (value) => {
        if (!value && value !== 0) return 'N/A';
        return new Intl.NumberFormat('es-MX', {
          style: 'currency',
          currency: 'MXN'
        }).format(value);
      };
      
      // Preparar datos para el gráfico de línea de ventas mensuales
      const monthlySalesChartData = computed(() => {
        if (!monthlySalesData.value || monthlySalesData.value.length === 0) {
          return { labels: [], datasets: [] };
        }
        
        try {
          const labels = monthlySalesData.value.map(item => {
            // Crear etiqueta para el mes (por ejemplo: 'Ene 2023')
            const monthNum = parseInt(item.month);
            const monthNames = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
            const monthName = monthNames[monthNum - 1] || 'Mes';
            return `${monthName} ${item.year}`;
          });
          
          const salesCountData = monthlySalesData.value.map(item => item.salesCount || 0);
          const unitsData = monthlySalesData.value.map(item => item.totalUnitsSold || 0);
          
          return {
            labels,
            datasets: [
              {
                label: 'Número de Ventas',
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                data: salesCountData,
                tension: 0.1
              },
              {
                label: 'Unidades Vendidas',
                borderColor: 'rgba(153, 102, 255, 1)',
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                data: unitsData,
                tension: 0.1
              }
            ]
          };
        } catch (error) {
          console.error('Error al procesar datos de ventas mensuales:', error);
          return { labels: [], datasets: [] };
        }
      });
      
      // Preparar datos para el gráfico de barras por ventas
      const salesChartData = computed(() => {
        if (!productSalesData.value || productSalesData.value.length === 0) {
          return { labels: [], datasets: [] };
        }
        
        try {
          // Limitar a los 5 productos con más ventas para una mejor visualización
          const topProducts = [...productSalesData.value]
            .sort((a, b) => b.totalSales - a.totalSales)
            .slice(0, 5);
          
          const labels = topProducts.map(item => item.productName);
          const salesData = topProducts.map(item => item.totalSales || 0);
          const revenueData = topProducts.map(item => item.totalRevenue || 0);
          
          return {
            labels,
            datasets: [
              {
                label: 'Ventas Totales',
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 1,
                data: salesData
              },
              {
                label: 'Ingresos Totales',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                data: revenueData
              }
            ]
          };
        } catch (error) {
          console.error('Error al procesar datos de productos:', error);
          return { labels: [], datasets: [] };
        }
      });
      
      // Opciones para el gráfico de barras por ventas
      const salesChartOptions = {
        plugins: {
          title: {
            display: true,
            text: 'Top 5 Productos por Ventas'
          }
        }
      };
      
      return {
        monthlySalesChartData,
        salesChartData,
        salesChartOptions,
        summaryData,
        loading,
        loadingSalesStats,
        loadingSummary,
        formatCurrency
      };
    }
  });
</script>
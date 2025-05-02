<template>
  <div class="chart-container">
    <canvas ref="chart"></canvas>
  </div>
</template>

<script>
  import { Chart, registerables } from 'chart.js';
  import { defineComponent, ref, onMounted, watch } from 'vue';

  // Registrar todos los componentes necesarios de Chart.js
  Chart.register(...registerables);

  export default defineComponent({
    name: 'LineChart',
    props: {
      chartData: {
        type: Object,
        required: true
      },
      options: {
        type: Object,
        default: () => ({})
      }
    },
    setup(props) {
      const chart = ref(null);
      let chartInstance = null;

      const createChart = () => {
        const ctx = chart.value.getContext('2d');
        
        // Destruir la instancia anterior si existe
        if (chartInstance) {
          chartInstance.destroy();
        }
        
        // Crear nueva instancia con los datos proporcionados
        chartInstance = new Chart(ctx, {
          type: 'line',
          data: props.chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Ventas Mensuales'
              }
            },
            ...props.options
          }
        });
      };

      // Crear gráfico cuando el componente está montado
      onMounted(() => {
        createChart();
      });

      // Actualizar gráfico cuando cambian los datos
      watch(() => props.chartData, () => {
        createChart();
      }, { deep: true });

      return {
        chart
      };
    }
  });
</script>

<style scoped>
  .chart-container {
    position: relative;
    height: 400px;
    width: 100%;
  }
</style>
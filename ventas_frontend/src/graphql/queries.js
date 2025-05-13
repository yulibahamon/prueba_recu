import gql from 'graphql-tag';

// Consulta para obtener todos los productos
export const ALL_PRODUCTS = gql`
  query {
    allProducts {
      id
      name
      price
    }
  }
`;

// Consulta para obtener todos los clientes
export const ALL_CUSTOMERS = gql`
  query {
    allCustomers {
      id
      name
      email
    }
  }
`;

// Consulta para obtener todas las ventas
export const ALL_SALES = gql`
  query {
    allSales {
      id
      product {
        id
        name
        price
      }
      quantity
      date
      totalAmount
    }
  }
`;

// Estadísticas de ventas por producto
export const PRODUCT_SALES_STATS = gql`
  query {
    productSalesStats {
      productId
      productName
      totalSales
      totalRevenue
    }
  }
`;

// Ventas mensuales
export const MONTHLY_SALES = gql`
  query {
    monthlySales {
      month
      salesCount
      totalUnitsSold
      totalRevenue
    }
  }
`;

// Resumen general de ventas
export const SALES_SUMMARY = gql`
  query {
    salesSummary {
      modeProduct {
        id
        name
        price
      }
      averageSale
      medianSale
      totalRevenue
      topCustomer {
        email
        id
        name
      }
      totalSales
    }
  }
`;

// Cliente con más compras
export const TOP_CUSTOMER = gql`
  query {
    topCustomer {
      customer {
        email
        id
        name
      }
      totalPurchases
      totalQuantity
      totalSpent
    }
  }
`;

// Producto con más ventas
export const TOP_PRODUCT = gql`
  query {
    topProduct {
      totalQuantity
      totalRevenue
      product {
        name
        id
        price
      }
      totalSales
    }
  }
`;
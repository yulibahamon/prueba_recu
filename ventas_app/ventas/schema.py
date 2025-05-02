import graphene
from graphene_django import DjangoObjectType
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth
import statistics
from datetime import datetime
from collections import Counter
from decimal import Decimal

from .models import Product, Customer, Sale

# Definir tipos para GraphQL
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price')

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email')

class SaleType(DjangoObjectType):
    total_amount = graphene.Float(description="Monto total de la venta")
    
    def resolve_total_amount(self, info):
        return float(self.product.price * self.quantity)
    
    class Meta:
        model = Sale
        fields = ('id', 'product', 'customer', 'quantity', 'date')

# Tipos para consultas estadísticas
class ProductSalesStatsType(graphene.ObjectType):
    product_id = graphene.Int(description="ID del producto")
    product_name = graphene.String(description="Nombre del producto")
    total_sales = graphene.Int(description="Cantidad total vendida")
    total_revenue = graphene.Float(description="Ingresos totales generados")

class MonthlySalesType(graphene.ObjectType):
    month = graphene.String(description="Mes de las ventas (formato YYYY-MM)")
    sales_count = graphene.Int(description="Cantidad de ventas en el mes")
    total_units_sold = graphene.Int(description="Cantidad total de productos vendidos")
    total_revenue = graphene.Float(description="Ingresos totales del mes")

class SalesSummaryType(graphene.ObjectType):
    total_sales = graphene.Int(description="Número total de ventas")
    total_revenue = graphene.Float(description="Ingresos totales")
    average_sale = graphene.Float(description="Valor promedio por venta")
    median_sale = graphene.Float(description="Valor mediano de ventas")
    mode_product = graphene.Field(ProductType, description="Producto más vendido (moda)")
    top_customer = graphene.Field(CustomerType, description="Cliente con más compras")

class TopCustomerDetailsType(graphene.ObjectType):
    customer = graphene.Field(CustomerType, description="Cliente con más compras")
    total_purchases = graphene.Int(description="Número total de compras realizadas")
    total_quantity = graphene.Int(description="Cantidad total de productos comprados")
    total_spent = graphene.Float(description="Cantidad total gastada")

class TopProductDetailsType(graphene.ObjectType):
    product = graphene.Field(ProductType, description="Producto más vendido")
    total_sales = graphene.Int(description="Número total de ventas del producto")
    total_quantity = graphene.Int(description="Cantidad total vendida")
    total_revenue = graphene.Float(description="Ingresos totales generados")

class Query(graphene.ObjectType):
    # Consultas básicas
    all_products = graphene.List(ProductType, description="Lista de todos los productos")
    all_customers = graphene.List(CustomerType, description="Lista de todos los clientes")
    all_sales = graphene.List(SaleType, description="Lista de todas las ventas")
    
    # Consultas estadísticas
    product_sales_stats = graphene.List(
        ProductSalesStatsType, 
        description="Estadísticas de ventas por producto"
    )
    monthly_sales = graphene.List(
        MonthlySalesType, 
        description="Ventas mensuales"
    )
    sales_summary = graphene.Field(
        SalesSummaryType,
        description="Resumen general de ventas"
    )
    top_customer = graphene.Field(
        TopCustomerDetailsType,
        description="Cliente con más compras"
    )
    top_product = graphene.Field(
        TopProductDetailsType,
        description="Producto más comprado"
    )
    
    # Resolvers para consultas básicas
    def resolve_all_products(self, info):
        return Product.objects.all()
    
    def resolve_all_customers(self, info):
        return Customer.objects.all()
    
    def resolve_all_sales(self, info):
        return Sale.objects.select_related('product', 'customer').all()
    
    # Resolvers para estadísticas
    def resolve_product_sales_stats(self, info):
        """
        Devuelve estadísticas de ventas por producto:
        - Cantidad total vendida
        - Ingresos totales generados
        """
        results = []
        
        for product in Product.objects.all():
            # Obtener todas las ventas del producto
            sales = Sale.objects.filter(product=product)
            
            # Calcular cantidad total vendida
            total_quantity = sales.aggregate(total=Sum('quantity'))['total'] or 0
            
            # Calcular ingresos totales
            total_revenue = sum(sale.product.price * sale.quantity for sale in sales)

            # Crear objeto de estadísticas
            results.append(ProductSalesStatsType(
                product_id=product.id,
                product_name=product.name,
                total_sales=total_quantity,
                total_revenue=float(total_revenue)
            ))
            
        return results
    
    def resolve_monthly_sales(self, info):
        """
        Devuelve ventas agrupadas por mes:
        - Cantidad de ventas
        - Cantidad total de productos vendidos
        - Ingresos totales
        """
        # Agrupar ventas por mes
        monthly_data = Sale.objects.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            sales_count=Count('id'),
            total_units_sold=Sum('quantity')
        ).order_by('month')
        
        results = []
        
        for data in monthly_data:
            # Obtener todas las ventas del mes
            month_sales = Sale.objects.filter(
                date__year=data['month'].year, 
                date__month=data['month'].month
            )
            
            # Calcular ingresos totales del mes
            total_revenue = sum(sale.product.price * sale.quantity for sale in month_sales)
            
            # Crear objeto de ventas mensuales
            results.append(MonthlySalesType(
                month=data['month'].strftime('%Y-%m'),
                sales_count=data['sales_count'],
                total_units_sold=data['total_units_sold'],
                total_revenue=float(total_revenue)
            ))
            
        return results
    
    def resolve_sales_summary(self, info):
        """
        Devuelve un resumen general de las ventas:
        - Total de ventas
        - Ingresos totales
        - Promedio de venta
        - Mediana de venta
        - Producto más vendido (moda)
        - Cliente con más compras
        """
        # Obtener todas las ventas
        sales = Sale.objects.all()
        
        if not sales.exists():
            return SalesSummaryType(
                total_sales=0,
                total_revenue=0.0,
                average_sale=0.0,
                median_sale=0.0,
                mode_product="",
                top_customer=None
            )
        
        # Total de ventas
        total_sales = sales.count()
        
        # Ingresos totales
        sale_amounts = [float(sale.product.price * sale.quantity) for sale in sales]
        total_revenue = sum(sale_amounts)
        
        # Promedio de venta
        average_sale = float(total_revenue) / total_sales if total_sales > 0 else 0.0
        
        # Mediana (valor de venta en la posición central)
        sale_amounts = [float(sale.product.price * sale.quantity) for sale in sales]
        median_sale = statistics.median(sale_amounts) if sale_amounts else 0.0
        
        # Moda (producto más vendido)
        # Primero obtener conteo por producto
        product_counts = sales.values('product').annotate(count=Sum('quantity')).order_by('-count')
        mode_product_id = product_counts.first()['product'] if product_counts.exists() else None
        mode_product = Product.objects.get(id=mode_product_id) if mode_product_id else None

        # Cliente con más compras
        customer_counts = sales.values('customer').annotate(count=Count('id')).order_by('-count')
        top_customer_id = customer_counts.first()['customer'] if customer_counts.exists() else None
        top_customer = Customer.objects.get(id=top_customer_id) if top_customer_id else None
        
        return SalesSummaryType(
            total_sales=total_sales,
            total_revenue=float(total_revenue),
            average_sale=average_sale,
            median_sale=median_sale,
            mode_product=mode_product,
            top_customer=top_customer
        )
    
    def resolve_top_customer(self, info):
        """
        Devuelve el cliente con más compras junto con información adicional:
        - Total de compras
        - Cantidad total de productos comprados
        - Total gastado
        """
        # Obtener el conteo de compras por cliente
        customer_purchase_counts = Sale.objects.values('customer').annotate(
            purchase_count=Count('id')
        ).order_by('-purchase_count')
        
        if not customer_purchase_counts.exists():
            return None
            
        # Obtener el ID del cliente con más compras
        top_customer_id = customer_purchase_counts.first()['customer']
        top_customer = Customer.objects.get(id=top_customer_id)
        
        # Obtener todas las ventas del cliente
        customer_sales = Sale.objects.filter(customer=top_customer)
        
        # Calcular métricas adicionales
        total_purchases = customer_sales.count()
        total_quantity = customer_sales.aggregate(total=Sum('quantity'))['total'] or 0
        total_spent = sum(float(sale.product.price * sale.quantity) for sale in customer_sales)
        
        return TopCustomerDetailsType(
            customer=top_customer,
            total_purchases=total_purchases,
            total_quantity=total_quantity,
            total_spent=total_spent
        )
    
    def resolve_top_product(self, info):
        """
        Devuelve el producto más vendido junto con información adicional:
        - Total de ventas
        - Cantidad total vendida
        - Ingresos totales generados
        """
        # Obtener el conteo de ventas por producto (en términos de cantidad)
        product_quantity_counts = Sale.objects.values('product').annotate(
            quantity_sold=Sum('quantity')
        ).order_by('-quantity_sold')
        
        if not product_quantity_counts.exists():
            return None
            
        # Obtener el ID del producto más vendido
        top_product_id = product_quantity_counts.first()['product']
        top_product = Product.objects.get(id=top_product_id)
        
        # Obtener todas las ventas del producto
        product_sales = Sale.objects.filter(product=top_product)
        
        # Calcular métricas adicionales
        total_sales = product_sales.count()  # Número de transacciones
        total_quantity = product_sales.aggregate(total=Sum('quantity'))['total'] or 0  # Unidades vendidas
        total_revenue = sum(float(sale.product.price * sale.quantity) for sale in product_sales)
        
        return TopProductDetailsType(
            product=top_product,
            total_sales=total_sales,
            total_quantity=total_quantity,
            total_revenue=total_revenue
        )
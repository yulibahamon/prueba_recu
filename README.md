# Sistema de Gestión de Ventas

## Descripción General
Este proyecto implementa un sistema de gestión de ventas utilizando Django y GraphQL. La aplicación permite manejar productos, clientes y ventas, ofreciendo una API GraphQL para consultar datos y estadísticas.


## Tecnologías Utilizadas
- **Django**: Framework web principal
- **GraphQL**: API query language con Graphene-Django
- **MySQL**: Base de datos relacional
- **CORS Headers**: Manejo de Cross-Origin Resource Sharing
- **Django Admin**: Interface administrativa

## Requisitos
- Python 3.12+
- MySQL
- pip (Python package manager)

## Instalación y Ejecución

1. Clonar el repositorio:
```sh
git clone <url-repositorio>
cd ventas_app
```

2. Crear y activar entorno virtual:
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```sh
pip install django graphene-django django-cors-headers mysqlclient
```

4. Configurar la base de datos:
- Crear base de datos MySQL llamada `ventas_db`
- Actualizar credenciales en `core/settings.py` si es necesario

5. Ejecutar migraciones:
```sh
python manage.py migrate
```

6. Cargar datos de prueba:
```sh
mysql -u root -p ventas_db < "datos prueba.sql"
```

7. Iniciar el servidor:
```sh
python manage.py runserver
```

## Estructura del Proyecto
```
ventas_app/
├── core/               # Configuración principal
├── ventas/            # Aplicación principal
│   ├── models.py      # Modelos de datos
│   ├── schema.py      # Definiciones GraphQL
│   └── admin.py       # Configuración admin
└── manage.py          # Script de gestión Django
```

## API GraphQL
Accesible en: `http://localhost:8000/graphql/`

Consultas disponibles:
- `allProducts`: Lista todos los productos
- `allCustomers`: Lista todos los clientes
- `allSales`: Lista todas las ventas
- `productSalesStats`: Estadísticas de ventas por producto
- `monthlySales`: Ventas mensuales
- `salesSummary`: Resumen general de ventas
- `top_customer`: Muestra el cliente con mayor ventas registradas
- `top_product`: Muestra el producto con mas ventas

## Panel de Administración
Accesible en: `http://localhost:8000/admin/`

## Notas de Desarrollo
- La aplicación utiliza Django 5.2
- Implementa CORS para permitir peticiones cross-origin
- Incluye sistema de estadísticas completo
- Base de datos prepoblada con datos de prueba
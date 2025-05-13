# Sistema de Gestión de Ventas

## Descripción General
Aplicación full-stack para gestión de ventas con:
- **Backend**: Django + GraphQL + MySQL
- **Frontend**: Vue.js + Apollo Client

## Estructura del Proyecto
```text
PRUEBA_RECU/
│
├── ventas_app/               # Backend Django (Python)
│   ├── core/                 # Configuración principal del proyecto
│   │   ├── settings.py       # Archivo de configuración y conexión  con base de datos 
│   │   ├── urls.py           # Rutas principales
│   │   └── ...
│   ├── ventas/               # App de gestión de ventas
│   │   ├── models.py         # Modelos de datos
│   │   ├── schema.py         # Definiciones GraphQL
│   │   └── ...
│   ├── manage.py             # Script de administración
│   └── requirements.txt      # Dependencias Python
│
├── ventas_frontend/          # Frontend Vue.js
│   ├── src/
|   │   ├── apollo/
|   │   │   └── index.js         # Configuración del cliente Apollo para GraphQL
|   │   ├── components/         # Componentes reutilizables
|   │   ├── views/             # Vistas principales (Dashboard, Sales, Statistics)
|   │   ├── router/
|   │   │   └── index.js       # Configuración de rutas de la aplicación
|   │   ├── store/
|   │   │   └── index.js       # Gestión del estado con Vuex
|   |   ├── graphql/
|   │   │   └── queries.js       # Definición de todas las consultas GraphQL
|   │   ├── App.vue           # Componente raíz
|   │   └── main.js          # Punto de entrada de la aplicación
|   ├── .env                 # Variables de entorno (URL del API)
|   └── package.json        # Dependencias y scripts
│
├── datos_prueba.sql          # Datos iniciales para MySQL
├── .gitignore               # Archivos ignorados por Git
└── README.md                # Documentación principal
```

## 📚 Tecnologías Utilizadas

### Backend (Django)
- **Django**: Framework web principal
- **MySQL**: Base de datos relacional
- **GraphQL** (graphene-django): Para la API
- **Otras librerías**:
  - `mysqlclient`: Conector MySQL para Python
  - `django-cors-headers`: Manejo de CORS
  - `django-filter`: Filtrado avanzado

### Frontend (Vue.js)
- **Vue 3**: Framework JavaScript
- **Apollo Client**: Conexión con GraphQL
- **Vuetify**: Componentes UI
- **Chart.js**: Visualización de datos
- **Vue Router**: Navegación
- **Vuex**: Gestión de estado

## 🚀 Configuración Inicial

### Requisitos Previos
- Python 3.8+
- Node.js 14+
- MySQL 8.0+
- pip y npm

**Clonar repositorio:**
```bash
git clone https://github.com/yulibahamon/prueba_recu.git
```

## Backend

1. Ingresar al proyecto Back ventas_app:
   ```bash
   cd prueba_recu/ventas_app
   ```

2. Crear y activar entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

3. Instalar dependencias:
    ```bash
    pip install django graphene-django django-cors-headers mysqlclient
    ```

4. Configurar la base de datos:
    - Crear base de datos MySQL llamada `ventas_db`
    - Actualizar credenciales en `core/settings.py` si es necesario
    ```bash
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'ventas_db', # Nombre de la Base de Datos creada en el paso anterior
                'USER': 'root',  # Cambia según tu configuración
                'PASSWORD': '',  # Cambia según tu configuración
                'HOST': 'localhost', # Cambia según tu configuración
                'PORT': '3306', # Cambia según tu configuración
            }
        }
    ```

5. Ejecutar migraciones:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Cargar datos de prueba:
    ```bash
    mysql -u root -p ventas_db < "datos prueba.sql"
    ```

7. Iniciar el servidor:
    ```bash
    python manage.py runserver
    ```

### API GraphQL
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

## Frontend 

Abre una nueva terminal para poder ejecutar el Front End y sigue los pasos

1. Ingresar al proyecto Front ventas_frontend:
    ```bash
    cd ../ventas_frontend
    ```
2. Instalar dependencias:
    ```bash
    npm install
    ```

3. Crea un archivo .env en la raiz del proyecto ventas_front
     ```bash
    VUE_APP_API_URL=http://localhost:8000/graphql/ # Modifica segun tu URL de Backend con Django
    ```

4. Iniciar aplicación:
    ```bash
    npm run serve
    ```

### Front End con Vue.js
Accesible en: `http://localhost:8080`

### Vistas Disponibles

- `Dashboard`: Vista principal que muestra un resumen general del sistema, incluyendo:
  - Tarjetas con métricas clave (total ventas, cantidad vendida, promedios)
  - Información del cliente y producto más destacado
  - Tabla de resumen de ventas por producto

- `Sales`: Implementa una tabla completa de ventas con:
  - Listado detallado de todas las transacciones
  - Funcionalidades de búsqueda y ordenamiento
  - Formato de fechas y valores monetarios
  - Vista de productos vendidos con sus cantidades

- `Statistics`: Proporciona visualizaciones y análisis estadísticos:
  - Gráfico de línea para ventas mensuales
  - Gráfico de barras para los 5 productos más vendidos
  - Métricas estadísticas detalladas (promedios, medianas, totales)
  - Indicadores de rendimiento clave

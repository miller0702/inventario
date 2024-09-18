# Inventario de Productos

## Descripción
Aplicación para gestionar el inventario de productos con autenticación por JWT y CRUD de usuarios y productos.

## Base de Datos
1. Dirigete a la ruta app/database, allí encontraras un archivo database.sql, el cual contiene el sql necesario para crear las tablas en mysql.

## Backend
- **Framework**: FastAPI
- **Base de datos**: MySQL
- **Dependencias**: `requirements.txt`

### Instrucciones para el Backend
1. Crear un entorno virtual y activar:
   ```bash
   python -m venv venv
   source venv/bin/activate  # en Windows usar `venv\Scripts\activate`

2. Instalar las dependencias:

   ```pip install -r requirements.txt```

3. Configurar la base de datos en .env

   ```DATABASE_URL=mysql://root:@localhost/inventario
   JWT_SECRET_KEY=tu_secreto_jwt
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30```

4. Descomentariza en el archivo main.py el código para crear un usuario por defecto.

5. Ejecutar la aplicación:

```venv\Scripts\activate```

```uvicorn app.main:app --reload```


## Estructura de Carpetas
├── app/
│   ├── main.py
│   ├── models/
│   │   ├── user.py
│   │   └── product.py
│   ├── routers/
│   │   ├── user_router.py
│   │   └── product_router.py
│   ├── schemas/
│   │   ├── user_schemas.py
│   │   └── product_schemas.py
│   ├── services/
│   │   ├── user_service.py
│   │   └── product_service.py
│   └── __init__.py
├── venv/
├── requirements.txt
└── .env




## Frontend
- **Framework**: Vue 3
- **Librería de componentes**: Element Plus
- **Estado global**: Vuex
- **Dependencias**: `package.json`

## Instrucciones para el Frontend

1. Instalar las dependencias:

   ```npm install```

2. Ejecutar la aplicación:

   ```npm run dev```


## Estructura de Carpetas
├── public/
│   └── index.html
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── Login.vue
│   │   ├── AdminLayout.vue
│   │   ├── UserList.vue
│   │   └── ProductList.vue
│   ├── views/
│   │   ├── LoginView.vue
│   │   ├── UsersView.vue
│   │   └── ProductsView.vue
│   ├── router/
│   │   └── index.js
│   ├── store/
│   │   └── index.js
│   ├── App.vue
│   └── main.js
├── .env
├── package.json
├── vue.config.js
└── yarn.lock

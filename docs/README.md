# Programacion 4
# Trabajo Practico 1 -  FastAPI + ABM

API REST desarrollada con FastAPI que implementa dos modulos de ABM (Alta, Baja y Modificacion) completos con almacenamiento en memoria y validacion mediante modelos Pydantic:
1. ABM de Usuarios (entidad provista por la catedra: id, name, is_active).
2. ABM de Productos (entidad propia de 5 campos: id, name, category, price, stock).

---

## Requisitos Previos

- Python 3.10 o superior instalado en el sistema.
- Gestor de paquetes pip.

---

## Instalacion y Puesta en Marcha

### 1. Clonar o ubicarse en el directorio del proyecto

```bash
cd "TP1 - FastAPI+ABM"
```

### 2. Crear un entorno virtual (recomendado)

En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

En Windows (CMD):
```cmd
python -m venv venv
.\venv\Scripts\activate.bat
```

En Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

Ejecutar el siguiente comando para instalar las librerias necesarias desde la carpeta docs:
```bash
pip install -r docs/requirements.txt
```

Las dependencias principales son:
- fastapi: Framework web para construir la API REST.
- uvicorn: Servidor ASGI de alto rendimiento.
- pydantic: Validacion de datos y definicion de esquemas.

### 4. Levantar la aplicacion

Iniciar el servidor de desarrollo con recarga automatica ante cambios:
```bash
python -m uvicorn main:app --reload
```
(O alternativamente `uvicorn main:app --reload` si el entorno virtual esta activo y tiene acceso directo a los binarios de Scripts).

El servidor quedara escuchando en:
`http://127.0.0.1:8000`

---

## Acceso a la Documentacion Interactiva (Swagger y ReDoc)

FastAPI genera automaticamente la documentacion OpenAPI interactiva:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Como probar los endpoints en Swagger UI:
1. Abrir el navegador web e ingresar a `http://127.0.0.1:8000/docs`.
2. Seleccionar el endpoint que se desea probar (por ejemplo, `GET /users` o `POST /products`).
3. Hacer clic en el boton "Try it out".
4. Si el endpoint requiere parametros de consulta (query params), parametros de ruta (path params) o un cuerpo JSON (request body), completar los valores en el formulario.
5. Hacer clic en el boton "Execute".
6. En la seccion "Responses" se visualizara el codigo de estado HTTP devuelto, el tiempo de respuesta y el JSON con los datos resultantes.

---

## Estructura del Proyecto

```text
TP1 - FastAPI+ABM/
|-- main.py              # Punto de entrada de la aplicacion e integracion de routers
|-- .gitignore           # Archivos y carpetas ignorados por git
|-- docs/
|   |-- README.md        # Documentacion e instrucciones de ejecucion
|   `-- requirements.txt # Lista de dependencias del proyecto
|-- models/
|   |-- __init__.py      # Exportacion de modelos
|   |-- users.py         # Modelos Pydantic para Usuarios (entidad catedra)
|   `-- products.py      # Modelos Pydantic para Productos (entidad propia: 5 campos)
`-- routers/
    |-- __init__.py      # Exportacion de routers
    |-- users.py         # Endpoints del ABM de Usuarios
    `-- products.py      # Endpoints del ABM de Productos
```

---

## Detalle de Endpoints Disponibles

### Endpoint Raiz
- `GET /`: Devuelve un mensaje de bienvenida y los enlaces a la documentacion.

---

### ABM de Usuarios (`/users`)

Entidad User definida por la catedra con los campos:
- `id` (int): Identificador unico del usuario.
- `name` (str): Nombre del usuario.
- `is_active` (bool): Estado activo/inactivo (por defecto True).

Endpoints:
1. `GET /users`: Listar usuarios.
   - Parametro de consulta opcional `is_active` (boolean):
     - `?is_active=true`: Devuelve unicamente usuarios activos.
     - `?is_active=false`: Devuelve unicamente usuarios inactivos.
     - Sin parametro: Devuelve todos los usuarios.
2. `GET /users/{id}`: Obtener los datos de un usuario por su ID (devuelve 404 si no existe).
3. `POST /users`: Dar de alta un nuevo usuario (status 201).
   - Ejemplo de body JSON:
     ```json
     {
       "id": 4,
       "name": "Maria Lopez",
       "is_active": true
     }
     ```
4. `PUT /users/{id}`: Modificar los datos de un usuario existente (status 200).
   - Ejemplo de body JSON:
     ```json
     {
       "name": "Maria Gomez",
       "is_active": false
     }
     ```
5. `PATCH /users/{id}`: Modificacion parcial de un usuario.
6. `DELETE /users/{id}`: Eliminar un usuario por su ID (status 200, devuelve 404 si no existe).

---

### ABM de Entidad Propia: Productos (`/products`)

Entidad Product con exactamente 5 campos:
- `id` (int): Identificador unico del producto.
- `name` (str): Nombre o descripcion del producto.
- `category` (str): Categoria del producto (ej: Computacion, Perifericos, Monitores).
- `price` (float): Precio unitario (debe ser mayor a cero).
- `stock` (int): Cantidad en inventario (debe ser mayor o igual a cero).

Endpoints:
1. `GET /products`: Listar productos con filtros combinables:
   - `category` (str): Filtrar por categoria exacta.
   - `name` (str): Buscar coincidencias parciales de texto en el nombre.
   - `in_stock` (bool): Filtrar por disponibilidad de stock (`true` para stock > 0, `false` para stock == 0).
   - `min_price` (float): Precio minimo.
   - `max_price` (float): Precio maximo.
2. `GET /products/{id}`: Obtener un producto por su ID (devuelve 404 si no existe).
3. `POST /products`: Dar de alta un nuevo producto (status 201).
   - Ejemplo de body JSON:
     ```json
     {
       "id": 5,
       "name": "Disco Solido SSD NVMe 1TB",
       "category": "Almacenamiento",
       "price": 110.0,
       "stock": 30
     }
     ```
4. `PUT /products/{id}`: Modificar los datos de un producto existente (status 200).
   - Ejemplo de body JSON:
     ```json
     {
       "name": "Disco Solido SSD NVMe 1TB Gen4",
       "category": "Almacenamiento",
       "price": 125.0,
       "stock": 25
     }
     ```
5. `PATCH /products/{id}`: Modificacion parcial de un producto.
6. `DELETE /products/{id}`: Eliminar un producto por su ID (status 200, devuelve 404 si no existe).

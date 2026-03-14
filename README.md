# Asignacion 03 - Seguridad en Bases de Datos

Laboratorio comparativo de **SQL Injection**: demuestra la diferencia entre una aplicacion vulnerable y una segura usando Flask + SQL Server.

---

## Estructura del Proyecto

```
asignacion03_seguridadbd/
├── docker-compose.yml       # Orquestador general (recomendado)
├── README.md
├── v1_vulnerable/           # App v1: vulnerable a SQL Injection
│   ├── app.py
│   ├── Dockerfile
│   ├── docker-compose.yml   # Ejecucion individual
│   └── templates/
│       └── index.html       # Pagina de documentacion interactiva
└── v2_segura/               # App v2: protegida con consultas parametrizadas
    ├── app.py
    ├── Dockerfile
    ├── docker-compose.yml   # Ejecucion individual
    └── templates/
        └── index.html       # Pagina de documentacion interactiva
```

---

## Requisitos Previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y en ejecucion
- Powershell (Windows 11)

---

## Ejecucion Rapida (Recomendada)

Desde la **raiz del proyecto**, ejecutar:

```powershell
docker-compose up -d --build
```

Esto levanta los 4 contenedores automaticamente:

| Contenedor       | Descripcion               | Puerto local |
|------------------|---------------------------|--------------|
| `sql_server_db`  | SQL Server 2022           | `1433`       |
| `redis_cache`    | Redis (cache)             | `6379`       |
| `web_vulnerable` | App Flask v1 Vulnerable   | `5001`       |
| `web_segura`     | App Flask v2 Segura       | `5002`       |

> Las apps esperan a que SQL Server este saludable antes de iniciar (healthcheck incluido).

---

## Paginas de Documentacion Interactiva

Cada version tiene una **pagina web** con explicaciones, ejemplos y botones para probar los ataques directamente desde el navegador.

| Version    | URL                     | Descripcion                          |
|------------|-------------------------|--------------------------------------|
| Vulnerable | http://localhost:5001   | Explica el ataque y permite probarlo |
| Segura     | http://localhost:5002   | Muestra como funciona la proteccion  |

Desde esas paginas puedes:
- Leer la explicacion de SQL Injection paso a paso
- Copiar payloads de ataque con un clic
- Navegar directamente al endpoint con el ataque pre-cargado
- Cambiar entre version vulnerable y segura

---

## Endpoints de la API

### Version 1 - Vulnerable (puerto 5001)

```
GET http://localhost:5001/cliente?apellido=<valor>
```

La respuesta incluye la `query_ejecutada` para ver el SQL generado:

```json
{
  "query_ejecutada": "SELECT name, database_id FROM sys.databases WHERE name LIKE 'm'",
  "resultados": [
    {"nombre_db": "master", "id": 1},
    {"nombre_db": "model",  "id": 3},
    {"nombre_db": "msdb",   "id": 4}
  ]
}
```

### Version 2 - Segura (puerto 5002)

```
GET http://localhost:5002/cliente?apellido=<valor>
```

---

## Demostrar SQL Injection (v1 Vulnerable)

La version 1 concatena el parametro `apellido` directamente al SQL sin ninguna proteccion.

### Ataque 1: OR 1=1 — leer TODAS las bases de datos

Abre en el navegador:
```
http://localhost:5001/cliente?apellido=' OR '1'='1'--
```

En Powershell:
```powershell
Invoke-RestMethod "http://localhost:5001/cliente?apellido=%27%20OR%20%271%27%3D%271%27--"
```

**SQL generado (peligroso):**
```sql
SELECT name, database_id FROM sys.databases
WHERE name LIKE '' OR '1'='1'--'
--                    ^^^^^^^^^ siempre verdadero — devuelve todo
```

### Ataque 2: UNION SELECT — extraccion de datos

```
http://localhost:5001/cliente?apellido=x' UNION SELECT name, database_id FROM sys.databases--
```

En Powershell:
```powershell
Invoke-RestMethod "http://localhost:5001/cliente?apellido=x%27%20UNION%20SELECT%20name%2C%20database_id%20FROM%20sys.databases--"
```

### Resultado esperado (v1)

La app devuelve **todas** las bases de datos del servidor, ignorando el filtro original.

---

## Verificar la Proteccion (v2 Segura)

La version 2 usa **consultas parametrizadas**. Los mismos payloads son tratados como texto literal.

```powershell
# Este payload es inocuo en v2
Invoke-RestMethod "http://localhost:5002/cliente?apellido=%27%20OR%20%271%27%3D%271%27--"
# Resultado: {"resultados": []}  — no existe esa base de datos literalmente
```

---

## Comparacion Tecnica

| Caracteristica           | v1 Vulnerable                              | v2 Segura                         |
|--------------------------|--------------------------------------------|-----------------------------------|
| Construccion de la query | Concatenacion directa de strings           | Marcadores de posicion `?`        |
| Riesgo de SQL Injection  | **SI**                                     | No                                |
| Query ejemplo            | `WHERE name LIKE '` + apellido + `'`       | `WHERE name LIKE ?` + parametro   |
| Respuesta                | Incluye `query_ejecutada` (educativo)      | Solo resultados                   |
| Pagina de documentacion  | http://localhost:5001 (roja)               | http://localhost:5002 (verde)     |

---

## Comandos Utiles

```powershell
# Ver el estado de todos los contenedores
docker ps

# Ver logs de la app vulnerable
docker-compose logs -f v1_vulnerable

# Ver logs de la app segura
docker-compose logs -f v2_segura

# Ver logs de SQL Server
docker-compose logs -f db

# Detener y eliminar todos los contenedores
docker-compose down

# Reconstruir imagenes y volver a levantar
docker-compose up -d --build
```

---

## Ejecucion Individual (Opcional)

Si se desea correr solo una version de forma independiente:

```powershell
# Desde la carpeta de la version deseada
cd v1_vulnerable
docker-compose up -d --build

# O la version segura
cd v2_segura
docker-compose up -d --build
```

> Nota: Cada carpeta tiene su propio `docker-compose.yml` con su propia instancia de SQL Server en el puerto `1433`.

---

## Credenciales de SQL Server

| Campo    | Valor              |
|----------|--------------------|
| Server   | `localhost,1433`   |
| Usuario  | `sa`               |
| Password | `Seguridad_2026!`  |
| Database | `master`           |

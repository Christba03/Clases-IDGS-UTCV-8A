# Practica: Backup, Restore, Export e Import en PostgreSQL con GUI

**Materia:** Base de Datos
**Herramientas:** Python 3, PostgreSQL, Docker, tkinter

---

## Objetivo

Aprender a realizar operaciones de respaldo, restauracion, exportacion e importacion de bases de datos PostgreSQL utilizando una interfaz grafica construida con Python y tkinter.

---

## Prerequisitos

| Software | Verificar con |
|---|---|
| Python 3.8+ | `python3 --version` |
| Docker | `docker --version` |
| PostgreSQL client tools (pg_dump, pg_restore, psql) | `pg_dump --version` |

---

## Paso 1 — Clonar el repositorio e instalar dependencias

```bash
git clone <URL_DEL_REPOSITORIO>
cd "base de datos"
pip install -r requirements.txt
```

El archivo `requirements.txt` instala `psycopg2-binary`, el driver de Python para PostgreSQL.

---

## Paso 2 — Levantar un contenedor de PostgreSQL con Docker

```bash
docker run -d \
  --name pg_test \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:16
```

Verificar que el contenedor esta corriendo:

```bash
docker ps
```

Deberias ver el contenedor `pg_test` con el puerto `5432` expuesto.

---

## Paso 3 — Crear una base de datos y tabla de prueba

Conectarse al contenedor y crear datos de ejemplo:

```bash
docker exec -i pg_test psql -U postgres <<'SQL'
CREATE DATABASE tienda;
\c tienda

CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    nombre     VARCHAR(50),
    apellido   VARCHAR(50),
    email      VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT NOW()
);

INSERT INTO clientes (nombre, apellido, email) VALUES
    ('Juan',   'Perez',    'juan@correo.com'),
    ('Maria',  'Lopez',    'maria@correo.com'),
    ('Carlos', 'Garcia',   'carlos@correo.com'),
    ('Ana',    'Martinez', 'ana@correo.com'),
    ('Luis',   'Hernandez','luis@correo.com');
SQL
```

---

## Paso 4 — Iniciar la interfaz grafica

```bash
python3 pg_tools_gui.py
```

Se abrira la ventana **PostgreSQL Tools**.

---

## Paso 5 — Configurar la conexion

En la barra superior de la ventana, completar los campos:

| Campo    | Valor       |
|----------|-------------|
| Host     | `localhost` |
| Port     | `5432`      |
| User     | `postgres`  |
| Password | `postgres`  |
| Database | `tienda`    |

Estos valores corresponden al contenedor Docker creado en el Paso 2.

---

## Paso 6 — Backup (Respaldo)

1. Ir a la pestana **Backup**.
2. En **Output file** escribir `backup_tienda.dump` (o usar **Browse...** para elegir la ruta).
3. En **Format** seleccionar `custom`.
4. Dejar **Schema only** desmarcado para respaldar datos y estructura.
5. Hacer clic en **Run Backup**.
6. En el area de log inferior debe aparecer: `Backup created: /ruta/backup_tienda.dump`.

### Variante: respaldo solo de estructura

Repetir el paso pero marcando **Schema only** y cambiando el nombre a `backup_schema.dump`. Esto genera un respaldo sin datos, util para replicar la estructura en otro servidor.

---

## Paso 7 — Restore (Restauracion)

1. Crear una base de datos vacia donde restaurar:

```bash
docker exec -i pg_test psql -U postgres -c "CREATE DATABASE tienda_copia;"
```

2. Ir a la pestana **Restore**.
3. En **Backup file** hacer clic en **Browse...** y seleccionar `backup_tienda.dump`.
4. En **Target DB** escribir `tienda_copia`.
5. Dejar **Clean** desmarcado (la base esta vacia).
6. Hacer clic en **Run Restore**.
7. El log debe mostrar: `Restore completed into database: tienda_copia`.

### Verificar la restauracion

```bash
docker exec -i pg_test psql -U postgres -d tienda_copia -c "SELECT * FROM clientes;"
```

Deberias ver los 5 registros originales.

---

## Paso 8 — Export (Exportar tabla a CSV)

1. Ir a la pestana **Export**.
2. En **Table** escribir `clientes`.
3. En **Output CSV** escribir `clientes.csv` (o usar **Browse...**).
4. Dejar **Custom query** vacio para exportar toda la tabla.
5. Hacer clic en **Run Export**.
6. El log debe mostrar: `Exported to /ruta/clientes.csv`.

### Verificar el CSV

Abrir el archivo `clientes.csv` con un editor de texto o con:

```bash
cat clientes.csv
```

Debe contener los encabezados y los 5 registros separados por comas.

### Variante: exportar con query personalizado

Repetir el paso, pero en **Custom query** escribir:

```sql
SELECT nombre, email FROM clientes WHERE cliente_id > 2
```

Esto exportara solo las columnas `nombre` y `email` de los clientes con ID mayor a 2.

---

## Paso 9 — Import (Importar CSV a tabla)

1. Crear una tabla destino para la importacion:

```bash
docker exec -i pg_test psql -U postgres -d tienda -c "
CREATE TABLE clientes_importados (
    cliente_id     INT,
    nombre         VARCHAR(50),
    apellido       VARCHAR(50),
    email          VARCHAR(100),
    fecha_registro TIMESTAMP
);"
```

2. Ir a la pestana **Import**.
3. En **Table** escribir `clientes_importados`.
4. En **Input CSV** hacer clic en **Browse...** y seleccionar `clientes.csv`.
5. Dejar **Truncate table first** desmarcado (la tabla esta vacia).
6. Hacer clic en **Run Import**.
7. El log debe mostrar: `Imported data into clientes_importados`.

### Verificar la importacion

```bash
docker exec -i pg_test psql -U postgres -d tienda -c "SELECT * FROM clientes_importados;"
```

### Variante: importar con truncate

Marcar **Truncate table first** y volver a hacer clic en **Run Import**. Esto vaciara la tabla antes de insertar, evitando duplicados.

---

## Paso 10 — Init (Inicializar base de datos con script SQL)

1. Crear un archivo `init_demo.sql` con el siguiente contenido:

```sql
CREATE DATABASE demo;
\c demo
CREATE TABLE productos (
    producto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    precio NUMERIC(10,2)
);
INSERT INTO productos (nombre, precio) VALUES ('Laptop', 15999.99), ('Mouse', 299.50);
```

2. Ir a la pestana **Init**.
3. En **SQL file** hacer clic en **Browse...** y seleccionar `init_demo.sql`.
4. Hacer clic en **Run Init**.
5. El log debe mostrar: `Database initialized using /ruta/init_demo.sql`.

### Verificar

```bash
docker exec -i pg_test psql -U postgres -d demo -c "SELECT * FROM productos;"
```

---

## Paso 11 — Limpieza

Al terminar la practica, detener y eliminar el contenedor:

```bash
docker stop pg_test && docker rm pg_test
```

---

## Estructura del proyecto

```
base de datos/
├── pg_tools.py          # Logica CLI (backup, restore, export, import, init)
├── pg_tools_gui.py      # Interfaz grafica con tkinter
├── requirements.txt     # Dependencias de Python
└── README.md            # Este archivo
```

---

## Resumen de operaciones

| Operacion | Que hace | Herramienta PostgreSQL |
|-----------|----------|----------------------|
| **Backup**  | Genera un archivo de respaldo de la base de datos | `pg_dump` |
| **Restore** | Restaura una base de datos desde un archivo de respaldo | `pg_restore` / `psql` |
| **Export**   | Exporta una tabla (o query) a un archivo CSV | `COPY ... TO STDOUT` |
| **Import**   | Importa datos desde un CSV hacia una tabla | `COPY ... FROM STDIN` |
| **Init**     | Ejecuta un script SQL para inicializar una base de datos | `psql` |

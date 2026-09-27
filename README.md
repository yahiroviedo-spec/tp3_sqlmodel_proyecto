# TP3 - SQLModel: Gestión de Oficinas y Personas

Práctica Profesionalizante I - Tecnicatura Superior en Desarrollo de Software
Instituto Técnico Superior Córdoba

Aplicación de consola que modela una relación uno a muchos entre **Oficina** y
**Persona** usando [SQLModel](https://sqlmodel.tiangolo.com/), implementada con
`Relationship()` / `back_populates` y con el ciclo CRUD completo sobre ambos
modelos.

## Estructura del proyecto

```
.
└── project/
    ├── __init__.py
    ├── models.py     # Oficina y Persona, con sus Relationship()
    ├── database.py   # engine y create_db_and_tables()
    └── app.py         # lógica de la aplicación / punto de entrada
```

## Instalación

1. Clonar el repositorio y ubicarse en la raíz del proyecto.
2. Crear y activar un entorno virtual:

   ```bash
   python -m venv venv

   # Linux / macOS
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

3. Instalar las dependencias:

   ```bash
   pip install sqlmodel
   ```

## Ejecución

Desde la raíz del proyecto (para que las importaciones relativas de `project/`
funcionen), ejecutar el módulo como paquete:

```bash
python -m project.app
```

Esto va a:

1. Crear el archivo `database.db` (SQLite) y las tablas `oficina` y `persona`.
2. Dar de alta oficinas y personas.
3. Ejecutar las consultas de lectura (listado por oficina, JOIN, filtro por
   nombre).
4. Reasignar una persona a otra oficina.
5. Eliminar una persona y una oficina, mostrando qué pasa al intentar borrar
   una oficina que todavía tiene personas asociadas.

Para volver a correr la demo desde cero, borrar `database.db` antes de
ejecutar el script nuevamente.

## Autor

Completar con nombre y comisión.

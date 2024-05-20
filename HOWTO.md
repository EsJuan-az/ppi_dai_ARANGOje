# 💻Carpetas:
Con la finalidad de ofrecer una mejor explicación acerca del proyecto, explicaré su estructura de carpetas.
- project/ 
    - app/ Aquí estarán todos los codigos fuente de la aplicación.
        - models.py: Este archivo guarda la estructura de las tablas en base de datos.
        - database.py: Codigos de inicialización y obtención de las sesiones de bdd.
        - env.py: Extrae las variables de entorno.
        - app.py: Clase que empaqueta la aplicación de fastAPI con todas sus rutas y funciones.
        - main.py: Archivo desde donde se instancia la app.
        - helpers/ Clases con metodos estáticos que ayudan a realizar funcionalidades de **analisis de datos** o errores.
        - services/ Instancias de la clase base_service.py usando los modelos de models.py y añadiendo cierta configuración. 
        - middlewares/ Codigos que se ejecutan en las rutas en caso de error.
        - routes/ Usa los metodos de sus respectivos servicios para servir respuestas en la web a peticiones específicas.
        - schemas/ Estructuras de datos que se recibirán dentro de la ruta para crear/actualizar filas.
    - migrations/ Codigo de sqlmodel y sqlalchemy, que al ejecutarse inicializarán la base de datos requerida.

# 📗Añadir dependencia y actualizar el requirements.txt
Tras la actualización de cualquier dependencia en el entorno de conda, ejecutaremos:
```bash
pip list --format=freeze > requirements.txt
```

# 🎞️ Migración a base de datos.
1. Instala alembic y entra en la carpeta project.
2. Ejecuta según tus necediades.
- Generar migración
```bash
alembic -c alembic_prod.ini revision --autogenerate -m "Nombre"
```
- Correr migraciones
```bash
alembic -c alembic_prod.ini upgrade head
```
- Remover migraciones
```bash
alembic -c alembic_prod.ini downgrade base
```
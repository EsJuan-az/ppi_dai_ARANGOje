# 📗Añadir dependencia y actualizar el requirements.yml
Tras la actualización de cualquier dependencia en el entorno de conda, ejecutaremos:
```bash
conda env export --no-builds --file project/requirements.yml
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
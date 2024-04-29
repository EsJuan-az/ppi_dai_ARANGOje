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

# 💻 Deploy en producción.
Para esto ejecutamos primero el contenedor. 
1. Abre el cliente de docker y ejecuta en consola:
```bash
docker-compose up -d --build prod_web
```
2. Ahora, tras ejecutar ésto y hacer login, etiquetamos la imagen y la subes.
```bash
docker tag [NOMBRE_IMAGEN]:[TAG] [USERNAME]/[REPO_NAME]:[TAG]
docker push [USERNAME]/[REPO_NAME]:[TAG]
```
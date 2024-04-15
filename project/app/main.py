from .app import App
# Obtenemos la app para escucharla con uvicorn.
fullsettings = App()
app = fullsettings.get_api()
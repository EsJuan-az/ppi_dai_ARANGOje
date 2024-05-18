from .app import App
from .env import PORT
# Obtenemos la app para escucharla con uvicorn.
fullsettings = App()
app = fullsettings.get_api()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
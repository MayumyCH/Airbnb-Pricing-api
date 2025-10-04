# Airbnb Pricing API

Esta es una API de FastAPI para predecir precios de alquileres de Airbnb.

## Instalación

1.  Crea un entorno virtual:

    ```bash
    python -m venv .venv
    source .venv/Scripts/activate
    ```

2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Ejecutar el Servidor Localmente

Ejecuta el siguiente comando en la raíz del proyecto:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

La documentacion en: `http://127.0.0.1:8000/docs`

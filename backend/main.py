import os
import logging
from datetime import datetime

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


load_dotenv()

app = FastAPI(title="NASA APOD Backend")
logger = logging.getLogger("nasa-apod")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _maybe_enable_system_certificates():
    """
    Some Windows environments (corporate/proxy) break cert chains for Python's certifi bundle.
    `truststore` lets requests use the OS certificate store instead.
    """
    if os.getenv("USE_SYSTEM_CERTS", "1") != "1":
        return
    try:
        import truststore

        truststore.inject_into_ssl()
    except Exception:
        # If truststore isn't available or fails, keep default behavior.
        return


_maybe_enable_system_certificates()


@app.get("/apod")
def get_apod(date: str):
    """
    Returns NASA APOD data for the given date (YYYY-MM-DD).
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Data inválida. Use o formato YYYY-MM-DD.")

    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="NASA_API_KEY não configurada no .env.")

    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key, "date": date}

    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.SSLError as e:
        logger.exception("SSL error contacting NASA")
        raise HTTPException(
            status_code=502,
            detail=(
                "Falha SSL ao acessar a NASA. "
                "Tente habilitar certificados do sistema (USE_SYSTEM_CERTS=1) "
                "ou configurar o proxy/certificado da rede. "
                f"Detalhe: {type(e).__name__}: {e}"
            ),
        )
    except requests.RequestException as e:
        logger.exception("Request error contacting NASA")
        raise HTTPException(
            status_code=502,
            detail=f"Erro ao consultar a API da NASA. Detalhe: {type(e).__name__}: {e}",
        )

    if response.status_code != 200:
        try:
            nasa_error = response.json()
        except ValueError:
            nasa_error = None

        message = "Erro retornado pela NASA."
        if isinstance(nasa_error, dict):
            # Many NASA APIs return an `error` object; keep it resilient.
            if isinstance(nasa_error.get("error"), dict) and nasa_error["error"].get("message"):
                message = str(nasa_error["error"]["message"])
            elif nasa_error.get("msg"):
                message = str(nasa_error["msg"])

        # Preserve upstream status for client-side troubleshooting (e.g. 429).
        raise HTTPException(status_code=response.status_code, detail=message)

    data = response.json()

    if data.get("media_type") != "image":
        raise HTTPException(
            status_code=400,
            detail="A APOD para essa data não é uma imagem. Tente outra data.",
        )

    result = {
        "date": data.get("date"),
        "title": data.get("title"),
        "explanation": data.get("explanation"),
        "url": data.get("url"),
        "hdurl": data.get("hdurl"),
    }

    return JSONResponse(content=result)


@app.get("/health")
def health_check():
    return {"status": "ok"}


import sys
import os
import threading
import webbrowser
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.api.src.routes.atualizar_estoque import router as atualizar_estoque_router
from app.api.src.routes.estoque_atual import router as produtos_router
from app.api.src.routes.vender import router as vendas_router
from app.api.src.routes.historico import router as historico_router
from app.api.src.routes.estoque_atual import router as estoque_atual_router
from app.api.src.routes.cobranca import router as cobranca_router
from app.api.src.routes.clientes import router as clientes_router

def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

app = FastAPI(
    title="Brownie API",
    version="1.0.0",
    description="API for managing Bonobrownie sales and inventory."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()
api_router.include_router(atualizar_estoque_router, prefix="/estoque", tags=["Estoque"])
api_router.include_router(produtos_router, prefix="/produtos", tags=["Produtos"])
api_router.include_router(vendas_router, prefix="/vendas", tags=["Vendas"])
api_router.include_router(historico_router, prefix="/historico", tags=["Histórico de Vendas"])
api_router.include_router(estoque_atual_router, prefix="/estoque", tags=["Estoque"])
api_router.include_router(cobranca_router, prefix="/cobranca", tags=["Cobrança"])
api_router.include_router(clientes_router, prefix="/clientes", tags=["Clientes"])
app.include_router(api_router, prefix="/api/v1")

@app.get("/ping")
def ping():
    return {"status": "ok"}

frontend_build_path = resource_path(os.path.join("probonobrownie-main", "dist"))
app.mount("/", StaticFiles(directory=frontend_build_path, html=True), name="static")

@app.get("/ping")
def ping():
    return {"status": "ok"}

def open_browser():
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=None)

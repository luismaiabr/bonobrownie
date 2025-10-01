from fastapi import APIRouter, Path
from pydantic import BaseModel, Field
from typing import List
from app.api.src.schemas.venda import Venda

router = APIRouter()

# --- Constante para definir o tamanho da página ---
ITENS_POR_PAGINA = 20

# ... (rota POST "/" existente) ...





class HistoricoVendasResponse(BaseModel):
    pagina: int = Field(..., description="Página atual retornada")
    total_registros: int = Field(..., description="Total de vendas no histórico")
    vendas: list[Venda] = Field(..., description="Lista de vendas da página")

@router.get(
    "/historico/{pagina}",
    response_model=HistoricoVendasResponse,
    summary="Obter Histórico de Vendas Paginado"
)
def obter_historico_de_vendas(
    *,
    pagina: int = Path(..., gt=0, description="O número da página para retornar")
)-> HistoricoVendasResponse:
    pass
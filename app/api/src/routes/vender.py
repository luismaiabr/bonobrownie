# src/brownie_api/api/v1/endpoints/vendas.py

from fastapi import APIRouter, status
router = APIRouter()
from app.api.src.schemas.venda import Venda, VendaCreate
@router.post(
    "/",
    response_model=Venda,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar uma Nova Venda",
    description="Cria um novo registro de venda e atualiza o estoque do produto correspondente."
)
def registrar_nova_venda(
    *,
    # db: Session = Depends(deps.get_db), (removido)
    venda_in: VendaCreate
) -> Venda:
    """
    Endpoint para registrar uma nova venda.

    - **cliente_id**: ID do cliente.
    - **produto_id**: ID do produto.
    - **unidades**: Quantidade vendida (deve ser maior que 0).
    - **prazo_dias**: Prazo em dias para o pagamento.
    - **valor_unitario**: Preço do produto no momento da venda.
    """
    #create venda
    return None
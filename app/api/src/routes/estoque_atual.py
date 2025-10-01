from typing import List
from app.api.src.schemas.produto import EstoqueRequest
import requests
from typing import Dict, Any
import json
from fastapi import APIRouter
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ0ZXBpeWpreHNhb3d3eW1vdHR3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTI2ODI4MCwiZXhwIjoyMDc0ODQ0MjgwfQ.NHrBblEdWdf1eiw_wN8TViYb6Ycj4lmVLUjRbMu7Ggo'
SUPABASE_URL = 'https://rtepiyjkxsaowwymottw.supabase.co'
router = APIRouter()
class StandardHTTPException(Exception):
    """
    Exceção aprimorada para encapsular erros de requisição HTTP,
    mostrando a resposta completa da API.
    """
    def __init__(self, detail: Dict[str, Any], status_code: int):
        self.detail = detail
        self.status_code = status_code
        # A mensagem base (super) continua simples, para logs concisos se necessário
        super().__init__(f"HTTP {status_code}: {self.detail.get('message', 'Erro desconhecido')}")

    def __str__(self):
        """
        Retorna uma representação em string detalhada e formatada do erro,
        incluindo a resposta completa da API.
        """
        # Formata o dicionário de detalhes em uma string JSON legível
        detailed_response = json.dumps(self.detail, indent=2, ensure_ascii=False)
        
        return (
            f"[ERRO HTTP {self.status_code}] {self.detail.get('message', 'Ocorreu um erro na requisição.')}\n"
            f"--- Resposta completa da API ---\n"
            f"{detailed_response}"
        )

# O router é prefixado com '/produtos' no arquivo principal da API
def _get_headers() -> dict:
    """Cria os cabeçalhos padrão para a autenticação na API do Supabase."""
    if not SUPABASE_KEY:
        raise ValueError("A chave do Supabase não foi definida.")
    
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Prefer": "return=representation",
    }

def obter_estoque(categoria_produto: str) -> int:
    """Obtém a quantidade em estoque de uma categoria de produto."""
    table_name = "Estoque"
    try:
        headers = _get_headers()
        url = f"{SUPABASE_URL}/rest/v1/{table_name}"
        params = {"categoria": f"eq.{categoria_produto}", "select": "quantidade"}
        
        response = requests.get(url, headers=headers, params=params, timeout=15.0)

        if response.status_code >= 400:
            try:
                detail = response.json()
            except json.JSONDecodeError:
                detail = {"message": response.text}
            raise StandardHTTPException(detail=detail, status_code=response.status_code)
        
        data = response.json()
        if not data:
            raise StandardHTTPException(
                detail={"message": f"A categoria de produto '{categoria_produto}' não foi encontrada."},
                status_code=404
            )
            
        return data[0]['quantidade']

    except requests.exceptions.RequestException as req_err:
        raise StandardHTTPException(detail={"message": f"Erro de conexão: {req_err}"}, status_code=503)
    except Exception as e:
        if isinstance(e, StandardHTTPException):
            raise
        raise StandardHTTPException(detail={"message": f"Erro inesperado: {e}"}, status_code=500)
@router.post(
    "/estoque_atual",
    summary="Obter Estoque Atual de Todos os Produtos",
    description="Retorna uma lista completa de todos os produtos e suas respectivas quantidades em estoque."
)
def obter_estoque_atual(
    req: EstoqueRequest,
    # db: Session = Depends(deps.get_db) (removido)
) -> int:
    """
    Endpoint para buscar o status atual do estoque de todos os produtos.
    """
    return obter_estoque(req.categoria)
# Venda schema
from pydantic import BaseModel, Field, computed_field
from datetime import datetime
from .msg import StatusPagamento
# --- Schemas de Venda ---

# Schema base com os campos que vêm do request de criação
class VendaBase(BaseModel):
    cliente_id: int = Field(..., description="ID do cliente que fez a compra")
    produto_id: int = Field(..., description="ID do produto vendido")
    unidades: int = Field(..., gt=0, description="Quantidade de unidades vendidas")
    prazo_dias: int = Field(..., ge=0, description="Prazo em dias para o pagamento")

# Schema para registrar uma nova venda
class VendaCreate(VendaBase):
    # O valor unitário no momento da venda é registrado para garantir consistência,
    # mesmo que o preço do produto mude no futuro.
    valor_unitario: float = Field(..., gt=0, description="Valor unitário do produto no momento da venda")

# Schema para atualizar o status de uma cobrança
class VendaUpdateStatus(BaseModel):
    status_pagamento: StatusPagamento = Field(..., description="Novo status do pagamento")
class CategoriaSchema(BaseModel):
    categoria: str = Field(..., description="Categoria do produto para filtrar o histórico")
class Venda(BaseModel):
    # --- Campos que espelham a tabela do Supabase ---
    id: int
    
    # Corrigido para datetime para ser compatível com timestamptz
    data_venda: datetime
    
    status_pagamento: bool
    cliente: str
    categoria_produto: str
    
    # Adicionado o campo que estava faltando
    qtd_unidades: int
    
    # Corrigido para ser um campo normal, lido do banco
    data_vencimento: datetime
    
    valor_unitario: float
    
    # Corrigido para ser um campo normal, lido do banco
    valor_total: float

    # Configuração para permitir a criação do modelo a partir de um objeto de banco de dados
    class Config:
        from_attributes = True
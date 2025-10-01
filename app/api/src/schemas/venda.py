# Venda schema
from pydantic import BaseModel, Field, computed_field
from datetime import date, timedelta
from .cliente import Cliente
from .produto import Produto
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


# Schema completo para leitura (usado no Histórico e nas Cobranças)
# Este schema é mais rico, incluindo objetos aninhados e campos calculados
class Venda(VendaBase):
    id: int
    data_venda: date
    status_pagamento: StatusPagamento
    valor_unitario: float # Valor no momento da venda

    # Inclui os dados completos do cliente e do produto para fácil exibição no frontend
    cliente: Cliente
    produto: Produto

    # Campo calculado para o valor total (Unidades * Valor Unitário)
    @computed_field
    @property
    def valor_total(self) -> float:
        return self.unidades * self.valor_unitario

    # Campo calculado para a data de vencimento (Data da Venda + Prazo)
    @computed_field
    @property
    def data_vencimento(self) -> date:
        return self.data_venda + timedelta(days=self.prazo_dias)

    class Config:
        from_attributes = True
import requests
from datetime import datetime
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status
from typing import Optional
import os
from dotenv import load_dotenv

router = APIRouter()

# --- Configuração do Supabase ---
load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Validação das variáveis de ambiente
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configuradas no .env")

# --- Funções Auxiliares ---
def _get_headers() -> dict:
    """
    Cria os cabeçalhos de autenticação para as requisições ao Supabase.
    """
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"  # ✅ Header importante!
    }

# --- Modelo de Dados de Entrada ---
class CobrancaInput(BaseModel):
    """
    Define a estrutura e validação dos dados de entrada para criar uma nova cobrança.
    
    Campos da tabela Cobranca no Supabase:
    - id: int8 (auto-gerado, não enviar)
    - created_at: timestamp (auto-gerado, não enviar)
    - status_pagamento: bool (obrigatório)
    - cliente: text (obrigatório)
    - vencimento: timestamp (obrigatório)
    - data_venda: timestamp (opcional)
    - valor: float8 (obrigatório)
    """
    cliente: str
    vencimento: datetime
    valor: float
    status_pagamento: bool  # ✅ Nome correto!
    data_venda: Optional[datetime] = None  # Campo adicional opcional

# --- Definição da Rota ---
@router.post(
    "/adicionar_cobranca",
    status_code=status.HTTP_201_CREATED,
    summary="Adiciona uma nova cobrança",
    description="Cria um novo registro na tabela 'Cobranca' com os dados fornecidos."
)
def adicionar_cobranca(cobranca: CobrancaInput):
    """
    Recebe os dados de uma nova cobrança e os insere na tabela 'Cobranca' do Supabase.
    
    Args:
        cobranca: Um objeto contendo 'cliente', 'vencimento', 'valor' e 'status'.
    
    Returns:
        Uma mensagem de sucesso com os dados da cobrança criada.
    
    Raises:
        HTTPException: Se a requisição ao Supabase falhar.
    """
    table_name = "Cobranca"
    
    # ✅ Converte para dict e serializa datetime para ISO format
    payload = cobranca.model_dump(mode="json")
    
    # Se você quiser enviar como array (para inserção em lote):
    # payload = [cobranca.model_dump(mode="json")]
    
    try:
        headers = _get_headers()
        url = f"{SUPABASE_URL}/rest/v1/{table_name}"
        
        response = requests.post(url, headers=headers, json=payload, timeout=15.0)
        
        # Para debug, você pode descomentar:
        # print(f"Status: {response.status_code}")
        # print(f"Response: {response.text}")
        
        response.raise_for_status()
        
        # Pega os dados retornados pelo Supabase
        data = response.json()
        
    except requests.exceptions.HTTPError as e:
        # Captura erros HTTP específicos (400, 404, 500, etc.)
        error_detail = e.response.text if e.response else str(e)
        # Log para debug
        print(f"Erro HTTP Status: {e.response.status_code if e.response else 'N/A'}")
        print(f"Payload enviado: {payload}")
        print(f"Response do Supabase: {error_detail}")
        raise HTTPException(
            status_code=e.response.status_code if e.response else 500,
            detail=f"Erro do Supabase: {error_detail}"
        )
    except requests.exceptions.RequestException as e:
        # Captura erros de conexão, timeout, etc.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro de comunicação com o Supabase: {e}"
        )
    
    return {
        "message": f"Cobrança para o cliente '{cobranca.cliente}' adicionada com sucesso!",
        "data": data
    }






























import requests
from datetime import datetime, timedelta

# URL base da sua API FastAPI
BASE_URL = "http://localhost:8000/api/v1/cobranca"  # Ajuste para sua URL (ex: http://127.0.0.1:8000)

def test_adicionar_cobranca():
    """
    Testa a rota POST /adicionar_cobranca
    """
    
    url = f"{BASE_URL}/adicionar_cobranca"
    
    # Payload de teste
    payload = {
        "cliente": "João Silva",
        "vencimento": (datetime.now() + timedelta(days=30)).isoformat(),
        "valor": 150.75,
        "status_pagamento": False
    }
    
    print("=" * 60)
    print("TESTE: POST /adicionar_cobranca")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Payload: {payload}")
    print()
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        print(response.json())
        
        if response.status_code == 201:
            print("\n✅ Cobrança adicionada com sucesso!")
        else:
            print(f"\n❌ Erro ao adicionar cobrança")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API.")
        print("Certifique-se de que o servidor FastAPI está rodando!")
        print("Execute: uvicorn main:app --reload")
    except requests.exceptions.Timeout:
        print("❌ Erro: Timeout na requisição")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def test_multiplas_cobrancas():
    """
    Testa a adição de múltiplas cobranças
    """
    
    url = f"{BASE_URL}/adicionar_cobranca"
    
    cobrancas = [
        {
            "cliente": "Maria Santos",
            "vencimento": (datetime.now() + timedelta(days=15)).isoformat(),
            "valor": 299.90,
            "status_pagamento": False,
            "data_venda": datetime.now().isoformat()
        },
        {
            "cliente": "Pedro Oliveira",
            "vencimento": (datetime.now() + timedelta(days=45)).isoformat(),
            "valor": 450.00,
            "status_pagamento": True
        },
        {
            "cliente": "Ana Costa",
            "vencimento": (datetime.now() + timedelta(days=60)).isoformat(),
            "valor": 125.50,
            "status_pagamento": False
        }
    ]
    
    print("\n" + "=" * 60)
    print("TESTE: Adicionando Múltiplas Cobranças")
    print("=" * 60)
    
    sucessos = 0
    erros = 0
    
    for i, payload in enumerate(cobrancas, 1):
        print(f"\n[{i}/{len(cobrancas)}] Adicionando cobrança para: {payload['cliente']}")
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 201:
                print(f"✅ Sucesso! - {response.json()['message']}")
                sucessos += 1
            else:
                print(f"❌ Erro {response.status_code}: {response.json()}")
                erros += 1
                
        except Exception as e:
            print(f"❌ Exceção: {e}")
            erros += 1
    
    print("\n" + "=" * 60)
    print("RESUMO:")
    print("=" * 60)
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    print(f"Total: {len(cobrancas)}")

def test_validacao_campos():
    """
    Testa a validação dos campos (payloads inválidos)
    """
    
    url = f"{BASE_URL}/adicionar_cobranca"
    
    payloads_invalidos = [
        {
            "nome": "Teste sem campo cliente",
            "payload": {
                "vencimento": datetime.now().isoformat(),
                "valor": 100.0,
                "status_pagamento": False
            },
            "erro_esperado": "Campo 'cliente' obrigatório"
        },
        {
            "nome": "Teste com valor negativo",
            "payload": {
                "cliente": "Teste",
                "vencimento": datetime.now().isoformat(),
                "valor": -50.0,
                "status_pagamento": False
            },
            "erro_esperado": "Valor pode ser negativo (validar no backend)"
        },
        {
            "nome": "Teste com data inválida",
            "payload": {
                "cliente": "Teste",
                "vencimento": "data-invalida",
                "valor": 100.0,
                "status_pagamento": False
            },
            "erro_esperado": "Formato de data inválido"
        }
    ]
    
    print("\n" + "=" * 60)
    print("TESTE: Validação de Campos")
    print("=" * 60)
    
    for test in payloads_invalidos:
        print(f"\n--- {test['nome']} ---")
        print(f"Payload: {test['payload']}")
        print(f"Erro esperado: {test['erro_esperado']}")
        
        try:
            response = requests.post(url, json=test['payload'], timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 422:
                print("✅ Validação funcionou corretamente!")
            elif response.status_code == 201:
                print("⚠️  Payload inválido foi aceito (considere adicionar validação)")
            
        except Exception as e:
            print(f"Exceção: {e}")

if __name__ == "__main__":
    print("\n🚀 INICIANDO TESTES DA API DE COBRANÇA\n")
    
    # Teste 1: Adicionar uma cobrança
    test_adicionar_cobranca()
    
    # Teste 2: Adicionar múltiplas cobranças
    test_multiplas_cobrancas()
    
    # Teste 3: Validação de campos
    test_validacao_campos()
    
    print("\n" + "=" * 60)
    print("✅ TESTES CONCLUÍDOS!")
    print("=" * 60)
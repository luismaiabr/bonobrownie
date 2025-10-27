# bonobrownie

# run with poetry run uvicorn app.main:app --reload

🚀 Como compilar e empacotar o projeto em um EXE
Estrutura geral do projeto
Backend Python: pasta app dentro de bonobrownie.

Frontend React/Vite: pasta probonobrownie-main.

O build final do React fica em probonobrownie-main/dist.

Passo a passo
Instale as dependências do frontend:

cd probonobrownie-main
npm install        # ou yarn install / pnpm install

Gere o build do frontend (React/Vite):
npm run build      # ou yarn build / pnpm build

# O build final ficará em: probonobrownie-main/dist
Volte para a pasta do backend:

cd ../bonobrownie
Instale as dependências do backend (Python/Poetry):

poetry install
Compile para EXE usando PyInstaller:

pyinstaller --onefile --noconsole --add-data "probonobrownie-main\\dist;probonobrownie-main/dist" app/main.py
Isso empacota o backend e o frontend juntos em um único arquivo .exe que será gerado na pasta dist.

Inclua seu arquivo .env junto ao EXE:

Configure as variáveis de ambiente (exemplo: chaves do Supabase) no .env.

Coloque o arquivo .env na mesma pasta do EXE.

Para rodar o EXE:

Basta dar dois cliques em main.exe (ou rodar pelo terminal).

O navegador será aberto automaticamente e a aplicação estará pronta para uso.
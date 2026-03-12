# SiteNASA

Aplicação simples que mostra a **Astronomy Picture of the Day (APOD)** da NASA para a data de nascimento informada pelo usuário.

O projeto é dividido em:

- **Backend** (`backend/`): API em FastAPI que consulta a API pública da NASA.
- **Frontend** (`frontend/`): página estática (HTML/CSS/JS) que consome o backend.

---

## Requisitos

- **Python 3.12+** (recomendado usar a mesma versão do seu ambiente virtual atual)
- Navegador moderno (Chrome, Edge, Firefox, etc.)
- Uma chave de API da NASA (grátis em: `https://api.nasa.gov`)

---

## 1. Configurando e rodando o backend

### 1.1. Criar (ou ativar) o ambiente virtual

Na raiz do projeto:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

> No PowerShell do Windows: `venv\Scripts\Activate.ps1` também funciona.

### 1.2. Instalar dependências

Com o ambiente virtual **ativado** dentro de `backend/`:

```bash
pip install -r requirements.txt
```

### 1.3. Configurar variáveis de ambiente

Dentro de `backend/`, crie um arquivo `.env` com o conteúdo:

```env
NASA_API_KEY=COLOQUE_SUA_CHAVE_AQUI
USE_SYSTEM_CERTS=1
```

- `NASA_API_KEY`: chave da API (obter em `https://api.nasa.gov`).
- `USE_SYSTEM_CERTS=1`: ajuda a evitar problemas de certificado em redes Windows corporativas.

### 1.4. Rodar o servidor FastAPI

Ainda em `backend/` e com o venv ativado:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

O backend ficará acessível em:

- `http://127.0.0.1:8000`

Rotas úteis para teste:

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/apod?date=2000-01-01`

---

## 2. Rodando o frontend

O frontend é puramente estático (HTML/CSS/JS), e foi pensado para rodar **apontando para o backend local** em `http://127.0.0.1:8000`.

O arquivo principal é `frontend/index.html`.

### 2.1. Abrir direto no navegador (modo simples)

Com o backend rodando:

1. Abra o explorador de arquivos no Windows.
2. Vá até a pasta do projeto `d:\-NASA-\frontend`.
3. Dê duplo clique em `index.html`.
4. O navegador abrirá a interface do site.
5. Informe sua data de nascimento e clique em **“Ver imagem”**.

> O JavaScript do frontend (`app.js`) já está configurado para chamar o backend em `http://127.0.0.1:8000`:
>
> ```js
> const API_BASE_URL = "http://127.0.0.1:8000";
> ```

### 2.2. Rodar com um servidor estático (opcional, recomendado)

Se quiser evitar problemas de CORS/cache, é possível servir a pasta `frontend/` com um servidor simples em Python:

Na raiz do projeto ou dentro de `frontend/`:

```bash
cd frontend
python -m http.server 5500
```

Depois acesse no navegador:

```text
http://127.0.0.1:5500/index.html
```

O comportamento será o mesmo, consumindo o backend em `http://127.0.0.1:8000`.

---

## 3. Fluxo completo (resumo)

1. **Backend**
   - `cd backend`
   - Ativar venv
   - `pip install -r requirements.txt`
   - Configurar `.env` com `NASA_API_KEY`
   - Rodar `uvicorn main:app --reload --host 127.0.0.1 --port 8000`

2. **Frontend**
   - `cd frontend`
   - Abrir `index.html` no navegador **ou**
   - `python -m http.server 5500` e acessar `http://127.0.0.1:5500/index.html`

Com isso você consegue rodar o projeto completo (back e front) localmente.


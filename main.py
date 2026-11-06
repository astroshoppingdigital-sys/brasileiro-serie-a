from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import obter_jogos_serie_a

app = FastAPI(
    title="Live Gol Série A - API Oficial",
    description="API em tempo real para rastrear partidas do Campeonato Brasileiro Série A",
    version="1.0.0"
)

# Configuração de CORS para permitir que o front-end consulte a API a cada 5s sem bloqueios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "status": "online",
        "mensagem": "API do Brasileirão Série A rodando perfeitamente!",
        "documentacao": "/docs",
        "endpoint_jogos": "/jogos/serie-a"
    }

# Endpoint padrão do seu projeto
@app.get("/jogos/serie-a")
def listar_jogos_serie_a():
    return obter_jogos_serie_a()

# Endpoint genérico para compatibilidade
@app.get("/api/jogos")
def listar_jogos_api():
    return obter_jogos_serie_a()

# Endpoint para filtrar apenas jogos AO VIVO
@app.get("/api/jogos/aovivo")
def listar_jogos_ao_vivo():
    todos = obter_jogos_serie_a()
    return [j for j in todos if j.get("status") == "LIVE"]

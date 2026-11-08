from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import obter_jogos_serie_a, obter_jogos_serie_b

app = FastAPI(
    title="Live Gol Série A & B - API Oficial",
    description="API em tempo real para rastrear partidas do Campeonato Brasileiro Séries A e B",
    version="1.0.0"
)

# Configuração de CORS para permitir que o front-end consulte a API sem bloqueios
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
        "mensagem": "API do Brasileirão Séries A e B rodando perfeitamente!",
        "documentacao": "/docs",
        "endpoint_serie_a": "/jogos/serie-a",
        "endpoint_serie_b": "/jogos/serie-b"
    }

# Endpoints da Série A
@app.get("/jogos/serie-a")
def listar_jogos_serie_a():
    return obter_jogos_serie_a()

@app.get("/api/jogos")
def listar_jogos_api():
    return obter_jogos_serie_a()

# Endpoint para a Série B
@app.get("/jogos/serie-b")
def listar_jogos_serie_b():
    return obter_jogos_serie_b()

# Endpoint para filtrar apenas jogos AO VIVO (Série A e B)
@app.get("/api/jogos/aovivo")
def listar_jogos_ao_vivo():
    todos = obter_jogos_serie_a() + obter_jogos_serie_b()
    return [j for j in todos if j.get("status") == "LIVE"]

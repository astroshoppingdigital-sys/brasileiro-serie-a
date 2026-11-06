from datetime import datetime
import requests

# Dicionário de escudos dos clubes
ESCUDOS_CLUBES = {
    "santos": "https://i.postimg.cc/j2tjm9P0/santos-fc.png",
    "sao_paulo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg/1200px-Brasao_do_Sao_Paulo_Futebol_Clube.svg.png",
    "corinthians": "https://upload.wikimedia.org/wikipedia/pt/b/b4/Corinthians_simbolo.png",
    "coritiba": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Coritiba_Foot_Ball_Club_logo.svg/1200px-Coritiba_Foot_Ball_Club_logo.svg.png",
    "gremio": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Gr%C3%AAmio_Foot-Ball_Porto-Alegrense_logo.svg/1200px-Gr%C3%AAmio_Foot-Ball_Porto-Alegrense_logo.svg.png",
    "vitoria": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Esporte_Clube_Vit%C3%B3ria_logo.svg/1200px-Esporte_Clube_Vit%C3%B3ria_logo.svg.png",
    "botafogo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Botafogo_de_Futebol_e_Regatas_logo.svg/1200px-Botafogo_de_Futebol_e_Regatas_logo.svg.png",
    "bragantino": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Red_Bull_Bragantino_logo.svg/1200px-Red_Bull_Bragantino_logo.svg.png",
    "chapecoense": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Associa%C3%A7%C3%A3o_Chapecoense_de_Futebol_logo.svg/1200px-Associa%C3%A7%C3%A3o_Chapecoense_de_Futebol_logo.svg.png",
    "mirassol": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Mirassol_Futebol_Clube_%28logo%29.svg/1200px-Mirassol_Futebol_Clube_%28logo%29.svg.png",
    "internacional": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Sport_Club_Internacional_logo.svg/1200px-Sport_Club_Internacional_logo.svg.png",
    "flamengo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Flamengo_brazão.svg/1200px-Flamengo_brazão.svg.png",
    "athletico_pr": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Athletico_Paranaense_logo_2019.svg/1200px-Athletico_Paranaense_logo_2019.svg.png",
    "atletico_mg": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Atletico_mineiro_galo.svg/1200px-Atletico_mineiro_galo.svg.png",
    "vasco": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Vasco_da_Gama_logo.svg/1200px-Vasco_da_Gama_logo.svg.png",
    "palmeiras": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Palmeiras_logo.svg/1200px-Palmeiras_logo.svg.png",
    "remo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Clube_do_Remo_logo.svg/1200px-Clube_do_Remo_logo.svg.png",
    "cruzeiro": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Cruzeiro_Esporte_Clube_%28logo%29.svg/1200px-Cruzeiro_Esporte_Clube_%28logo%29.svg.png",
    "bahia": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Esporte_Clube_Bahia_logo.svg/1200px-Esporte_Clube_Bahia_logo.svg.png",
    "fluminense": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Fluminense_FC_escudo.svg/1200px-Fluminense_FC_escudo.svg.png"
}

LOGO_SITE = "https://i.postimg.cc/K8PR1kCv/Gemini-Generated-Image-hozi2rhozi2rhozi-removebg-preview.png"

def obter_jogos_serie_a(api_endpoint: str = None):
    """
    Retorna todos os confrontos da Série A com horários oficiais e captura de placar em tempo real.
    """
    dados_api_externa = None
    if api_endpoint:
        try:
            resposta = requests.get(api_endpoint, timeout=3)
            if resposta.status_code == 200:
                dados_api_externa = resposta.json()
        except Exception as err:
            print(f"Aviso: Não foi possível obter dados da API externa ({err}).")

    # Valores padrão ou capturados da API de placares ao vivo
    placar_home_atual = 4
    placar_away_atual = 1
    status_jogo_atual = "LIVE"

    if dados_api_externa:
        placar_home_atual = int(dados_api_externa.get("score_home", 4))
        placar_away_atual = int(dados_api_externa.get("score_away", 1))
        status_jogo_atual = str(dados_api_externa.get("status_partida", "LIVE")).upper()

    jogos_cadastrados = [
        # ==========================================
        # --- 34ª RODADA ---
        # ==========================================
        {
            "id": "bragantino-santos",
            "homeTeam": {"name": "Red Bull Bragantino", "logo": ESCUDOS_CLUBES["bragantino"]},
            "awayTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "date": "02/11/2026",
            "time": "20:00",
            "timestamp_jogo": "2026-11-02T20:00:00",
            "score": {"fullTime": {"home": 2, "away": 1}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "FINISHED",
            "statusCustomizado": "Partida Finalizada",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "verde",
            "destaque_banner": False
        },
        {
            "id": "chapecoense-mirassol",
            "homeTeam": {"name": "Chapecoense", "logo": ESCUDOS_CLUBES["chapecoense"]},
            "awayTeam": {"name": "Mirassol", "logo": ESCUDOS_CLUBES["mirassol"]},
            "date": "03/11/2026",
            "time": "19:30",
            "timestamp_jogo": "2026-11-03T19:30:00",
            "score": {"fullTime": {"home": 1, "away": 2}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "FINISHED",
            "statusCustomizado": "Partida Finalizada",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "verde",
            "destaque_banner": False
        },
        {
            "id": "internacional-coritiba",
            "homeTeam": {"name": "Internacional", "logo": ESCUDOS_CLUBES["internacional"]},
            "awayTeam": {"name": "Coritiba", "logo": ESCUDOS_CLUBES["coritiba"]},
            "date": "03/11/2026",
            "time": "21:30",
            "timestamp_jogo": "2026-11-03T21:30:00",
            "score": {"fullTime": {"home": 1, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "FINISHED",
            "statusCustomizado": "Partida Finalizada",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "verde",
            "destaque_banner": False
        },
        {
            "id": "flamengo-gremio",
            "homeTeam": {"name": "Flamengo", "logo": ESCUDOS_CLUBES["flamengo"]},
            "awayTeam": {"name": "Grêmio", "logo": ESCUDOS_CLUBES["gremio"]},
            "date": "Hoje",
            "time": "19:30",
            "timestamp_jogo": "2026-11-05T19:30:00",
            # Placar dinâmico atualizado em tempo real (4 x 1)
            "score": {"fullTime": {"home": placar_home_atual, "away": placar_away_atual}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": status_jogo_atual,
            "statusCustomizado": "2º Tempo",
            "status_transmissao": "ONLINE",
            "cor_indicador": "amarelo",
            "destaque_banner": True
        },
        {
            "id": "athletico-pr-vasco",
            "homeTeam": {"name": "Athletico-PR", "logo": ESCUDOS_CLUBES["athletico_pr"]},
            "awayTeam": {"name": "Vasco", "logo": ESCUDOS_CLUBES["vasco"]},
            "date": "04/11/2026",
            "time": "19:30",
            "timestamp_jogo": "2026-11-04T19:30:00",
            "score": {"fullTime": {"home": 1, "away": 3}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "FINISHED",
            "statusCustomizado": "Partida Finalizada",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "verde",
            "destaque_banner": False
        },
        {
            "id": "botafogo-atletico-mg",
            "homeTeam": {"name": "Botafogo", "logo": ESCUDOS_CLUBES["botafogo"]},
            "awayTeam": {"name": "Atlético-MG", "logo": ESCUDOS_CLUBES["atletico_mg"]},
            "date": "04/11/2026",
            "time": "21:30",
            "timestamp_jogo": "2026-11-04T21:30:00",
            "score": {"fullTime": {"home": 1, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "FINISHED",
            "statusCustomizado": "Partida Finalizada",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "verde",
            "destaque_banner": False
        },
        {
            "id": "sao-paulo-corinthians",
            "homeTeam": {"name": "São Paulo", "logo": ESCUDOS_CLUBES["sao_paulo"]},
            "awayTeam": {"name": "Corinthians", "logo": ESCUDOS_CLUBES["corinthians"]},
            "date": "Ontem",
            "time": "21:30",
            "timestamp_jogo": "2026-11-04T21:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "FINISHED",
            "statusCustomizado": "Partida Finalizada",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "verde",
            "destaque_banner": False
        },
        {
            "id": "palmeiras-remo",
            "homeTeam": {"name": "Palmeiras", "logo": ESCUDOS_CLUBES["palmeiras"]},
            "awayTeam": {"name": "Remo", "logo": ESCUDOS_CLUBES["remo"]},
            "date": "05/11/2026",
            "time": "19:30",
            "timestamp_jogo": "2026-11-05T19:30:00",
            "score": {"fullTime": {"home": 6, "away": 1}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "FINISHED",
            "statusCustomizado": "Partida Finalizada",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "verde",
            "destaque_banner": False
        },
        {
            "id": "cruzeiro-bahia",
            "homeTeam": {"name": "Cruzeiro", "logo": ESCUDOS_CLUBES["cruzeiro"]},
            "awayTeam": {"name": "Bahia", "logo": ESCUDOS_CLUBES["bahia"]},
            "date": "05/11/2026",
            "time": "21:30",
            "timestamp_jogo": "2026-11-05T21:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "vitoria-fluminense",
            "homeTeam": {"name": "Vitória", "logo": ESCUDOS_CLUBES["vitoria"]},
            "awayTeam": {"name": "Fluminense", "logo": ESCUDOS_CLUBES["fluminense"]},
            "date": "06/11/2026",
            "time": "20:00",
            "timestamp_jogo": "2026-11-06T20:00:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },

        # ==========================================
        # --- 35ª RODADA ---
        # ==========================================
        {
            "id": "mirassol-atletico-mg",
            "homeTeam": {"name": "Mirassol", "logo": ESCUDOS_CLUBES["mirassol"]},
            "awayTeam": {"name": "Atlético-MG", "logo": ESCUDOS_CLUBES["atletico_mg"]},
            "date": "18/11/2026",
            "time": "18:30",
            "timestamp_jogo": "2026-11-18T18:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "coritiba-santos",
            "homeTeam": {"name": "Coritiba", "logo": ESCUDOS_CLUBES["coritiba"]},
            "awayTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "date": "18/11/2026",
            "time": "19:30",
            "timestamp_jogo": "2026-11-18T19:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "flamengo-athletico-pr",
            "homeTeam": {"name": "Flamengo", "logo": ESCUDOS_CLUBES["flamengo"]},
            "awayTeam": {"name": "Athletico-PR", "logo": ESCUDOS_CLUBES["athletico_pr"]},
            "date": "18/11/2026",
            "time": "20:30",
            "timestamp_jogo": "2026-11-18T20:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "cruzeiro-palmeiras",
            "homeTeam": {"name": "Cruzeiro", "logo": ESCUDOS_CLUBES["cruzeiro"]},
            "awayTeam": {"name": "Palmeiras", "logo": ESCUDOS_CLUBES["palmeiras"]},
            "date": "18/11/2026",
            "time": "20:30",
            "timestamp_jogo": "2026-11-18T20:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "corinthians-botafogo",
            "homeTeam": {"name": "Corinthians", "logo": ESCUDOS_CLUBES["corinthians"]},
            "awayTeam": {"name": "Botafogo", "logo": ESCUDOS_CLUBES["botafogo"]},
            "date": "18/11/2026",
            "time": "21:30",
            "timestamp_jogo": "2026-11-18T21:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "gremio-bahia",
            "homeTeam": {"name": "Grêmio", "logo": ESCUDOS_CLUBES["gremio"]},
            "awayTeam": {"name": "Bahia", "logo": ESCUDOS_CLUBES["bahia"]},
            "date": "18/11/2026",
            "time": "21:30",
            "timestamp_jogo": "2026-11-18T21:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "remo-chapecoense",
            "homeTeam": {"name": "Remo", "logo": ESCUDOS_CLUBES["remo"]},
            "awayTeam": {"name": "Chapecoense", "logo": ESCUDOS_CLUBES["chapecoense"]},
            "date": "19/11/2026",
            "time": "19:00",
            "timestamp_jogo": "2026-11-19T19:00:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "vasco-internacional",
            "homeTeam": {"name": "Vasco", "logo": ESCUDOS_CLUBES["vasco"]},
            "awayTeam": {"name": "Internacional", "logo": ESCUDOS_CLUBES["internacional"]},
            "date": "19/11/2026",
            "time": "19:30",
            "timestamp_jogo": "2026-11-19T19:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "vitoria-bragantino",
            "homeTeam": {"name": "Vitória", "logo": ESCUDOS_CLUBES["vitoria"]},
            "awayTeam": {"name": "Red Bull Bragantino", "logo": ESCUDOS_CLUBES["bragantino"]},
            "date": "19/11/2026",
            "time": "19:30",
            "timestamp_jogo": "2026-11-19T19:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "sao-paulo-fluminense",
            "homeTeam": {"name": "São Paulo", "logo": ESCUDOS_CLUBES["sao_paulo"]},
            "awayTeam": {"name": "Fluminense", "logo": ESCUDOS_CLUBES["fluminense"]},
            "date": "19/11/2026",
            "time": "21:30",
            "timestamp_jogo": "2026-11-19T21:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },

        # ==========================================
        # --- 36ª RODADA ---
        # ==========================================
        {
            "id": "atletico-mg-corinthians",
            "homeTeam": {"name": "Atlético-MG", "logo": ESCUDOS_CLUBES["atletico_mg"]},
            "awayTeam": {"name": "Corinthians", "logo": ESCUDOS_CLUBES["corinthians"]},
            "date": "22/11/2026",
            "time": "16:00",
            "timestamp_jogo": "2026-11-22T16:00:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "athletico-pr-remo",
            "homeTeam": {"name": "Athletico-PR", "logo": ESCUDOS_CLUBES["athletico_pr"]},
            "awayTeam": {"name": "Remo", "logo": ESCUDOS_CLUBES["remo"]},
            "date": "22/11/2026",
            "time": "18:30",
            "timestamp_jogo": "2026-11-22T18:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "bahia-coritiba",
            "homeTeam": {"name": "Bahia", "logo": ESCUDOS_CLUBES["bahia"]},
            "awayTeam": {"name": "Coritiba", "logo": ESCUDOS_CLUBES["coritiba"]},
            "date": "22/11/2026",
            "time": "18:30",
            "timestamp_jogo": "2026-11-22T18:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "botafogo-sao-paulo",
            "homeTeam": {"name": "Botafogo", "logo": ESCUDOS_CLUBES["botafogo"]},
            "awayTeam": {"name": "São Paulo", "logo": ESCUDOS_CLUBES["sao_paulo"]},
            "date": "23/11/2026",
            "time": "20:00",
            "timestamp_jogo": "2026-11-23T20:00:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "chapecoense-cruzeiro",
            "homeTeam": {"name": "Chapecoense", "logo": ESCUDOS_CLUBES["chapecoense"]},
            "awayTeam": {"name": "Cruzeiro", "logo": ESCUDOS_CLUBES["cruzeiro"]},
            "date": "23/11/2026",
            "time": "20:00",
            "timestamp_jogo": "2026-11-23T20:00:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "fluminense-mirassol",
            "homeTeam": {"name": "Fluminense", "logo": ESCUDOS_CLUBES["fluminense"]},
            "awayTeam": {"name": "Mirassol", "logo": ESCUDOS_CLUBES["mirassol"]},
            "date": "23/11/2026",
            "time": "20:00",
            "timestamp_jogo": "2026-11-23T20:00:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "internacional-vitoria",
            "homeTeam": {"name": "Internacional", "logo": ESCUDOS_CLUBES["internacional"]},
            "awayTeam": {"name": "Vitória", "logo": ESCUDOS_CLUBES["vitoria"]},
            "date": "23/11/2026",
            "time": "20:00",
            "timestamp_jogo": "2026-11-23T20:00:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "palmeiras-flamengo",
            "homeTeam": {"name": "Palmeiras", "logo": ESCUDOS_CLUBES["palmeiras"]},
            "awayTeam": {"name": "Flamengo", "logo": ESCUDOS_CLUBES["flamengo"]},
            "date": "23/11/2026",
            "time": "20:30",
            "timestamp_jogo": "2026-11-23T20:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "bragantino-vasco",
            "homeTeam": {"name": "Red Bull Bragantino", "logo": ESCUDOS_CLUBES["bragantino"]},
            "awayTeam": {"name": "Vasco", "logo": ESCUDOS_CLUBES["vasco"]},
            "date": "23/11/2026",
            "time": "20:30",
            "timestamp_jogo": "2026-11-23T20:30:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        {
            "id": "santos-gremio",
            "homeTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "awayTeam": {"name": "Grêmio", "logo": ESCUDOS_CLUBES["gremio"]},
            "date": "23/11/2026",
            "time": "21:00",
            "timestamp_jogo": "2026-11-23T21:00:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        }
    ]

    return jogos_cadastrados

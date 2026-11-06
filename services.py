from datetime import datetime
import requests

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
    "palmeiras": "https://i.postimg.cc/qMXDNBzY/palmeiras.png",
    "remo": "https://i.postimg.cc/sD7dwR1R/Clube-do-Remo-svg.webp",
    "cruzeiro": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Cruzeiro_Esporte_Clube_%28logo%29.svg/1200px-Cruzeiro_Esporte_Clube_%28logo%29.svg.png",
    "bahia": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Esporte_Clube_Bahia_logo.svg/1200px-Esporte_Clube_Bahia_logo.svg.png",
    "fluminense": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Fluminense_FC_escudo.svg/1200px-Fluminense_FC_escudo.svg.png"
}

LOGO_SITE = "https://i.postimg.cc/K8PR1kCv/Gemini-Generated-Image-hozi2rhozi2rhozi-removebg-preview.png"

def obter_jogos_serie_a():
    jogos_cadastrados = [
        # Jogos passados já finalizados corretamente na aba Encerrados (Azul Gelo)
        {
            "id": "sao-paulo-corinthians",
            "homeTeam": {"name": "São Paulo", "logo": ESCUDOS_CLUBES["sao_paulo"]},
            "awayTeam": {"name": "Corinthians", "logo": ESCUDOS_CLUBES["corinthians"]},
            "date": "Ontem",
            "time": "21:30",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "FINISHED",
            "statusCustomizado": "Partida Finalizada",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "azul-gelo",
            "destaque_banner": False
        },
        {
            "id": "palmeiras-remo",
            "homeTeam": {"name": "Palmeiras", "logo": ESCUDOS_CLUBES["palmeiras"]},
            "awayTeam": {"name": "Remo", "logo": ESCUDOS_CLUBES["remo"]},
            "date": "05/11/2026",
            "time": "19:30",
            "score": {"fullTime": {"home": 6, "away": 1}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "FINISHED",
            "statusCustomizado": "Partida Finalizada",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "azul-gelo",
            "destaque_banner": False
        },

        # --- JOGOS DO SANTOS (FORA E NA VILA) NOS AGENDADOS ---
        # Jogo fora: Vitória x Santos
        {
            "id": "vitoria-santos",
            "homeTeam": {"name": "Vitória", "logo": ESCUDOS_CLUBES["vitoria"]},
            "awayTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "date": "30/11/2026",
            "time": "20:00",
            "timestamp_jogo": "2026-11-30T20:00:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "status_transmissao": "OFFLINE",
            "cor_indicador": "cinza",
            "destaque_banner": False
        },
        # Jogo fora: Coritiba x Santos
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
        # Jogo na Vila (Santos mandante): Santos x Grêmio
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

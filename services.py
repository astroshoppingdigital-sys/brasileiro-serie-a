from datetime import date
import requests

# Links oficiais dos escudos e da logo fornecidos por você
ESCUDOS_CLUBES = {
    "santos": "https://i.postimg.cc/j2tjm9P0/santos-fc.png",
    "coritiba": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Coritiba_Foot_Ball_Club_logo.svg/1200px-Coritiba_Foot_Ball_Club_logo.svg.png",
    "gremio": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Gr%C3%AAmio_Foot-Ball_Porto-Alegrense_logo.svg/1200px-Gr%C3%AAmio_Foot-Ball_Porto-Alegrense_logo.svg.png",
    "vitoria": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Esporte_Clube_Vit%C3%B3ria_logo.svg/1200px-Esporte_Clube_Vit%C3%B3ria_logo.svg.png",
    "botafogo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Botafogo_de_Futebol_e_Regatas_logo.svg/1200px-Botafogo_de_Futebol_e_Regatas_logo.svg.png"
}

LOGO_SITE = "https://i.postimg.cc/K8PR1kCv/Gemini-Generated-Image-hozi2rhozi2rhozi-removebg-preview.png"

def obter_jogos_serie_a(api_endpoint: str = None):
    """
    Retorna a lista exclusiva dos próximos jogos do Santos solicitados,
    com escudos personalizados e logomarca do site.
    """
    jogos_agendados_santos = [
        {
            "id": "coritiba-santos-2026",
            "homeTeam": {"name": "Coritiba", "logo": ESCUDOS_CLUBES["coritiba"]},
            "awayTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "date": "18/11",
            "time": "19:30",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado - 18/11, 19:30",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE"
        },
        {
            "id": "gremio-santos-2026",
            "homeTeam": {"name": "Grêmio", "logo": ESCUDOS_CLUBES["gremio"]},
            "awayTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "date": "23/11",
            "time": "21:00",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado - 23/11, 21:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE"
        },
        {
            "id": "vitoria-santos-2026",
            "homeTeam": {"name": "EC Vitória", "logo": ESCUDOS_CLUBES["vitoria"]},
            "awayTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "date": "29/11",
            "time": "A confirmar",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado - 29/11",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE"
        },
        {
            "id": "botafogo-santos-2026",
            "homeTeam": {"name": "Botafogo", "logo": ESCUDOS_CLUBES["botafogo"]},
            "awayTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "date": "02/12",
            "time": "A confirmar",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado - 02/12",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE"
        }
    ]

    try:
        return jogos_agendados_santos
    except Exception as e:
        print(f"Erro ao carregar os jogos: {e}")
        return jogos_agendados_santos

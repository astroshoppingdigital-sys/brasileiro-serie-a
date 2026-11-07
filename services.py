from fastapi import HTTPException
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

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
    # URL alterada para o Campeonato Brasileiro Série A (bra.1) mantendo a mesma lógica da Série B
    url = "https://site.web.api.espn.com/apis/site/v2/sports/soccer/bra.1/scoreboard"
    try:
        resposta = requests.get(url, headers=HEADERS, timeout=15)
        resposta.raise_for_status()
        dados = resposta.json()

        jogos_formatados = []
        events = dados.get("events", [])

        for event in events:
            competition = event.get("competitions", [{}])[0]
            competitors = competition.get("competitors", [])

            mandante = next((c for c in competitors if c.get("homeAway") == "home"), {})
            visitante = next((c for c in competitors if c.get("homeAway") == "away"), {})

            status_obj = event.get("status", {})
            status_type = status_obj.get("type", {})

            state = status_type.get("state")  # "pre", "in", "post"
            completed = status_type.get("completed", False)
            description = status_type.get("description", "")

            # Tratativa blindada de estado idêntica à da Série B
            if state == "post" or completed:
                status_real = "FINISHED"
                status_customizado = "Partida Finalizada"
                cor_indicador = "azul-gelo"
            elif state == "in":
                status_real = "LIVE"
                status_customizado = "Ao Vivo"
                cor_indicador = "verde-abacate"
            elif state == "pre":
                status_real = "SCHEDULED"
                status_customizado = "Agendado"
                cor_indicador = "cinza"
            else:
                status_real = "SCHEDULED"
                status_customizado = description or "Aguardando"
                cor_indicador = "cinza"

            nome_mandante = mandante.get("team", {}).get("displayName", "")
            nome_visitante = visitante.get("team", {}).get("displayName", "")

            jogos_formatados.append({
                "id": event.get("id"),
                "homeTeam": {
                    "name": nome_mandante,
                    "logo": mandante.get("team", {}).get("logo")
                },
                "awayTeam": {
                    "name": nome_visitante,
                    "logo": visitante.get("team", {}).get("logo")
                },
                "date": event.get("date"),
                "time": status_obj.get("displayClock"),
                "stadium": competition.get("venue", {}).get("fullName"),
                "score": {
                    "fullTime": {
                        "home": int(mandante.get("score", 0) if mandante.get("score") is not None else 0),
                        "away": int(visitante.get("score", 0) if visitante.get("score") is not None else 0)
                    }
                },
                "logo_transmissao_offline": LOGO_SITE,
                "status": status_real,
                "statusCustomizado": status_customizado,
                "status_transmissao": "OFFLINE",
                "cor_indicador": cor_indicador,
                "destaque_banner": False,
                "tempo_jogo": status_obj.get("displayClock"),
                "periodo": status_obj.get("period")
            })

        return jogos_formatados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar jogos: {str(e)}")

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
    Retorna os próximos jogos do Santos com horários, escudos personalizados,
    logomarca do site e suporte a atualizações dinâmicas de tempo, placar e status (Ao Vivo, Intervalo, Encerrado).
    """
    if not api_endpoint:
        api_endpoint = "https://sua-api-de-futebol.com/api/jogos"

    # Lista base dos próximos jogos do Santos configurados
    jogos_santos = [
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
            "id": "santos-botafogo-2026",
            "homeTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "awayTeam": {"name": "Botafogo", "logo": ESCUDOS_CLUBES["botafogo"]},
            "date": "02/12",
            "time": "15:00",  # Horário ajustado para as 15h com o Santos mandante na Vila Belmiro
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado - 02/12, 15:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE"
        }
    ]

    try:
        # Tenta buscar atualizações em tempo real da API externa (placar, intervalo, fim de jogo, etc.)
        response = requests.get(api_endpoint, timeout=5)
        if response.status_code == 200:
            data = response.json()
            partidas_api = data.get("matches", data.get("response", data if isinstance(data, list) else []))
            
            # Cruzamento opcional para atualizar dinamicamente se a API externa fornecer dados da partida em andamento
            for jogo in jogos_santos:
                for p in partidas_api:
                    # Lógica para identificar o confronto correspondente
                    home_api = str(p.get("homeTeam", {}).get("name", "")).lower()
                    away_api = str(p.get("awayTeam", {}).get("name", "")).lower()
                    
                    if "santos" in home_api or "santos" in away_api:
                        api_status = str(p.get("status", "")).upper()
                        
                        # Se a API externa indicar que o jogo está ao vivo, em intervalo ou encerrado, atualiza o status dinamicamente
                        if api_status in ["LIVE", "IN_PLAY", "HT", "PAUSED", "FINISHED", "FT"]:
                            jogo["status"] = "LIVE" if api_status != "FINISHED" else "FINISHED"
                            
                            # Atualiza placar real vindo da API
                            if "score" in p:
                                jogo["score"] = p["score"]
                                
                            # Customiza o status do tempo (1º tempo, intervalo, 2º tempo, fim de jogo)
                            if api_status in ["HT", "PAUSED"]:
                                jogo["statusCustomizado"] = "Intervalo"
                            elif api_status in ["FINISHED", "FT"]:
                                jogo["statusCustomizado"] = "Encerrado"
                                jogo["status_transmissao"] = "OFFLINE"
                            else:
                                minuto = p.get("minute", "Ao Vivo")
                                jogo["statusCustomizado"] = f"AO VIVO • {minuto}"
                                jogo["status_transmissao"] = "AO_VIVO"

        return jogos_santos

    except Exception as e:
        print(f"Erro ao consultar API externa em tempo real: {e}")
        # Retorna a lista configurada com horários e escudos mesmo se a API externa falhar
        return jogos_santos
